"""
Created on Jun 26, 2015

@author: hsorby
"""
import logging
import subprocess
import os.path
import platform

from PySide import QtCore

from mapclient.settings.definitions import GIT_EXE, VIRTUAL_ENV_PATH, \
    PYSIDE_UIC_EXE, PYSIDE_RCC_EXE, USE_EXTERNAL_GIT
from mapclient.core.utils import which


logger = logging.getLogger(__name__)


class ApplicationChecks(object):

    def __init__(self, options):
        self._options = options
        self._report = 'Failure: This test failed'

    def doCheck(self):
        return False

    def report(self):
        return self._report


class WizardToolChecks(ApplicationChecks):

    title = 'Wizard Tool'

    def doCheck(self):
        uic_result = False
        rcc_result = False
        self._report = ''  # {0}\n'.format(self.title)
        try:
            pyside_uic = self._options[PYSIDE_UIC_EXE]
            try:
                p = subprocess.Popen([pyside_uic, '--help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = p.communicate()
                if stdout:
                    logger.info(stdout)
                if stderr:
                    logger.info(stderr)
            except OSError as e:
                # Trying to run the uic.py script?
                p = subprocess.Popen(['python', pyside_uic, '--help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = p.communicate()
                if stdout:
                    logger.info(stdout)
                if stderr:
                    logger.info(stderr)
#c:\python35amd64\Scripts\pyside-uic.EXE
            return_code = p.returncode
            if return_code == 0:
                uic_result = True
                self._report += "'{0}' successfully ran.".format(pyside_uic)
            else:
                self._report += "'{0}' did not execute successfully, returned '{1}' on exit.".format(pyside_uic, return_code)
        except Exception as e:
            self._report += "The test for pyside-uic [tested executable '{0}'] did not execute successfully, but caused an exception:\n{1}".format(pyside_uic, e)
        if self._report:
            self._report += '\n'
        try:
            pyside_rcc = self._options[PYSIDE_RCC_EXE]
            p = subprocess.Popen([pyside_rcc, '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            _, stderr = p.communicate()
            return_code = p.returncode
            # pyside-rcc returns 1 for all program executions that don't actual compile resources.
            if return_code == 1 and 'Resource Compiler for Qt version' in stderr.decode('utf-8'):
                rcc_result = True
                self._report += "'{0}' successfully ran.".format(pyside_rcc)
            else:
                self._report += "'{0}' did not execute successfully, returned '{1}' on exit.".format(pyside_rcc, return_code)
        except Exception as e:
            self._report += "The test for pyside-rcc [tested executable '{0}'] did not execute successfully, but caused an exception:\n{1}".format(pyside_rcc, e)

        return uic_result and rcc_result


class VirtualEnvChecks(ApplicationChecks):

    title = 'Virtual Environment'

    def doCheck(self):
        venv_path = self._options[VIRTUAL_ENV_PATH]
        result = False
        pip_exe = getPipExecutable(venv_path)
        if ' ' in venv_path or not venv_path:
            self._report = "'{0}' is not a valid virtual environment path.".format(venv_path)
        elif pip_exe is None:
            self._report = "pip executable not found."
        else:
            result = True
            self._report = "'{0}' is a valid virtual environment.".format(venv_path)

        return result


class VCSChecks(ApplicationChecks):

    title = 'Version Control'

    def doCheck(self):
        result = False
        self._report = ''

        if self._options[USE_EXTERNAL_GIT]:
            try:
                vcs_tool = self._options[GIT_EXE]
                p = subprocess.Popen([vcs_tool, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, _ = p.communicate()
                return_code = p.returncode
                if return_code == 0 and 'git version' in stdout.decode('utf-8'):
                    result = True
                    self._report += "'{0}' successfully ran.".format(vcs_tool)
                else:
                    self._report += "'{0}' did not execute successfully, returned '{1}' on exit.".format(vcs_tool, return_code)
            except Exception as e:
                self._report += "'{0}' did not execute successfully, caused exception:\n{1}".format(vcs_tool, e)
        else:
            try:
                import dulwich
                ver = dulwich.__version__
                self._report += "Internal Git version '{0}.{1}.{2}' successfully ran.".format(ver[0], ver[1], ver[2])
                result = True
            except ImportError:
                self._report += "Internal Git did not execute successfully."

        return result

def runChecks(options):
    check_status = True
    checks_wizard = WizardToolChecks(options)
    if not checks_wizard.doCheck():
        check_status = False

    checks_venv = VirtualEnvChecks(options)
    if not checks_venv.doCheck():
        check_status = False

    checks_vcs = VCSChecks(options)
    if not checks_vcs.doCheck():
        check_status = False

    return check_status


def getPipExecutable(venv_path):
    python_version = platform.python_version_tuple()
    if os.name == 'nt':
        int_directory = 'Scripts'
    else:
        int_directory = 'bin'
    pip_exe = which(os.path.join(venv_path, int_directory, 'pip' + python_version[0] + '.' + python_version[1]))
    return pip_exe


def getActivateScript(venv_path):
    if os.name == 'nt':
        int_directory = 'Scripts'
        suffix = '.bat'
    else:
        int_directory = 'bin'
        suffix = ''
    activate_script = which(os.path.join(venv_path, int_directory, 'activate' + suffix))
    return activate_script


def getPySideUicExecutable():
    pyside_uic_potentials = ['pyside-uic', 'py2side-uic', 'py3side-uic', 'pyside-uic-py2']
    for pyside_uic_potential in pyside_uic_potentials:
        pyside_uic = which(pyside_uic_potential)  #  self._options[PYSIDE_UIC_EXE]
        if pyside_uic:
            p = subprocess.Popen([pyside_uic, '--help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            _, _ = p.communicate()
            return_code = p.returncode
            if return_code == 0:
                return pyside_uic

    # Fallback for Anaconda??
    try:
        from PySide.scripts import uic
        uic_script = uic.__file__

        return uic_script
    except ImportError:
        pass

    return None


def getPySideRccExecutable():
    if os.name == 'nt':
        pyside_rcc_directory = os.path.dirname(QtCore.__file__)
        pyside_rcc_potentials = [os.path.join(pyside_rcc_directory, 'pyside-rcc'), 'pyside-rcc']
    else:
        pyside_rcc_potentials = ['pyside-rcc']

    for pyside_rcc_potential in pyside_rcc_potentials:
        pyside_rcc = which(pyside_rcc_potential)
        if pyside_rcc is not None:
            p = subprocess.Popen([pyside_rcc, '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            _, stderr = p.communicate()
            return_code = p.returncode
            # pyside-rcc returns 1 for all program executions that don't actually compile resources.
            if return_code == 1 and 'Resource Compiler for Qt version' in stderr.decode('utf-8'):
                return pyside_rcc

    return None



