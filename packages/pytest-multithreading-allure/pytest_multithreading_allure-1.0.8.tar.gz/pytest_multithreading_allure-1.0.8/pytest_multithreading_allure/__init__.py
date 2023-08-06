from six import with_metaclass
import threading

from pluggy import PluginManager
from allure_commons import _hooks

import pytest
from allure_pytest.helper import AllureTitleHelper
from allure_pytest.listener import AllureListener
from allure_commons.reporter import AllureReporter
import allure_pytest
import allure_commons

class MetaPluginManager(type):
    @staticmethod
    def get_plugin_manager():
        if not hasattr(MetaPluginManager, 'plugin_manager'):

            MetaPluginManager.plugin_manager = PluginManager('allure')
            MetaPluginManager.plugin_manager.add_hookspecs(_hooks.AllureUserHooks)
            MetaPluginManager.plugin_manager.add_hookspecs(_hooks.AllureDeveloperHooks)

        return MetaPluginManager.plugin_manager

    def __getattr__(cls, attr):
        pm = MetaPluginManager.get_plugin_manager()
        return getattr(pm, attr)


class plugin_manager(with_metaclass(MetaPluginManager)):
    pass


class ThreadLocalAllureListener(threading.local, AllureListener):
    def __init__(self,config):
        super(ThreadLocalAllureListener, self).__init__(config)


class ThreadLocalAllureReporter(threading.local, AllureReporter):
    def __init__(self):
        super(ThreadLocalAllureReporter, self).__init__()


@pytest.mark.tryfirst
def pytest_configure(config):
    title_helper = AllureTitleHelper()
    plugin_manager.register(title_helper)

    allure_commons.plugin_manager = plugin_manager
    allure_commons._core.plugin_manager = plugin_manager
    allure_commons.reporter.plugin_manager = plugin_manager
    allure_commons._allure.plugin_manager = plugin_manager

    allure_pytest.plugin.AllureReporter = ThreadLocalAllureReporter
    allure_pytest.plugin.AllureListener = ThreadLocalAllureListener