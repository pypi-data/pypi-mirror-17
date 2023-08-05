# -*- coding: utf-8 -*-
# Copyright (c) 2016 Sqreen. All Rights Reserved.
# Please refer to our terms for more information: https://www.sqreen.io/terms.html
""" Helpers to retrieve runtime informations
"""
import os
import sys
import datetime
import platform
import threading

from logging import getLogger

try:
    from pip import get_installed_distributions
    HAS_PIP = True
except ImportError:
    # We don't have pip, fallback on pkg_resources
    HAS_PIP = False
    import pkg_resources

    def get_installed_distributions():
        """ Mimic pip.get_installed_distributions using pkg_resources
        """
        return pkg_resources.working_set


import sqreen

LOGGER = getLogger(__name__)


def _format_datetime_isoformat(datetime_object):
    """ Take a datetime and return it as isoformat
    """
    return datetime_object.isoformat()


class RuntimeStorage(object):
    """ Object for storing runtime informations like the current request processed
    """

    def __init__(self):
        self.local = threading.local()
        self._current_request_initializer()

    def _current_request_initializer(self):
        if not hasattr(self.local, "current_request"):
            setattr(self.local, "current_request", None)

    def store_request(self, request):
        """ Store a request, whatever its kind in a thread-safe way
        """
        LOGGER.debug("Store request %s", request)
        self._current_request_initializer()
        self.local.current_request = request

    def clear_request(self):
        """ Clear the stored request in a thread-safe way
        """
        LOGGER.debug("Clear request %s", getattr(self.local, 'current_request'))
        if hasattr(self.local, "current_request"):
            self.local.current_request = None

    def get_current_request(self):
        """ Return current processed request
        """
        self._current_request_initializer()
        return self.local.current_request


runtime = RuntimeStorage()


class RuntimeInfos(object):
    """ Helper to collect and return environement informations about the
    runtime
    """

    def all(self):
        """ Returns aggregated infos from the environment
        """
        resultat = {'various_infos': {}}
        resultat.update(self._agent())
        resultat.update(self._framework())
        resultat.update(self._os())
        resultat.update(self._runtime())
        resultat['various_infos'].update(self._time())
        resultat['various_infos'].update(self._dependencies())
        resultat['various_infos'].update(self._process())
        return resultat

    @staticmethod
    def _dependencies():
        """ Returns informations about the installed python dependencies
        """
        dep = [{
            'name': package.project_name,
            'version': package.version
        } for package in get_installed_distributions()]
        return {"dependencies": dep}

    @staticmethod
    def _time():
        """ Returns informations about the current time
        """
        return {'time': _format_datetime_isoformat(datetime.datetime.utcnow())}

    @staticmethod
    def _agent():
        """ Returns informations about the agent
        """
        return {'agent_type': 'python', 'agent_version': sqreen.__version__}

    @staticmethod
    def _get_package_version(package_name):
        for package in get_installed_distributions():
            if package.project_name == package_name:
                return package.version

    def _framework(self):
        """ Returns informations about the web framework
        """
        flask = self._get_package_version('Flask')
        django = self._get_package_version('Django')
        pyramid = self._get_package_version('pyramid')

        if django:
            return {'framework_type': 'Django', 'framework_version': django}
        elif flask:
            return {'framework_type': 'Flask', 'framework_version': flask}
        elif pyramid:
            return {'framework_type': 'pyramid', 'framework_version': pyramid}
        else:
            return {'framework_type': None, 'framework_version': None}

    @staticmethod
    def _os():
        """ Returns informations about the os
        """

        # Compute the OS version
        if sys.platform == 'darwin':
            base_os_version = 'Mac OS X {}'.format(platform.mac_ver()[0])
        elif 'linux' in sys.platform:
            base_os_version = '{0[0]} {0[1]}'.format(platform.linux_distribution())
        else:
            base_os_version = ''

        os_version = '{}/{}'.format(base_os_version, '/'.join(os.uname()))
        return {'os_type': '{}-{}'.format(platform.machine(), sys.platform),
                'os_version': os_version,
                'hostname': platform.node()}

    @staticmethod
    def _runtime():
        """ Returns informations about the python runtime
        """
        python_build = platform.python_build()
        version = '{} ({}, {})'.format(platform.python_version(), python_build[0],
                                       python_build[1])
        return {'runtime_type': platform.python_implementation(),
                'runtime_version': version}

    @staticmethod
    def _process():
        """ Returns informations about the current process
        """
        return {
            'pid': os.getpid(),
            'ppid': os.getppid(),
            'euid': os.geteuid(),
            'egid': os.getegid(),
            'uid': os.getuid(),
            'gid': os.getgid(),
            # sys.argv is not always available
            'name': getattr(sys, 'argv', [None])[0]
        }
