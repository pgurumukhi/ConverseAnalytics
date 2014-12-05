__author__ = 'Shridhar'

from browsermobproxy import Server
from selenium import webdriver
import time
import test_steps
import os

_test_data_dir = os.path.join(os.path.split(__file__)[0], "testdata")

class ad_driver():
    _driver = None
    _server = None
    _proxy = None

    def __init__(self, path_to_batch, browser="chrome"):

        """ start browsermob proxy """
        self._server = Server(path_to_batch)
        self._server.start()
        self._proxy = self._server.create_proxy()

        """ Init browser profile """
        if browser is "chrome":
            PROXY = "localhost:%s" % self._proxy.port  # IP:PORT or HOST:PORT
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--proxy-server=%s' % PROXY)
            self._driver = webdriver.Chrome(chrome_options=chrome_options)
        elif browser is "ff":
            profile = webdriver.FirefoxProfile()
            driver = webdriver.Firefox(firefox_profile=profile, proxy=proxy)
        else:
            print "Please set 'browser' variable to any of the value \n 'chrome', 'ff' !"
        self._driver.maximize_window()
        self._driver.implicitly_wait(20)

    def execute(self, test):

        self._proxy.new_har(test["name"])
        self._driver.get(_test_data_dir + os.sep + test['file'])
        time.sleep(2)
        callToTestMethod = getattr(test_steps, test["name"])
        callToTestMethod(self._driver)
        har = self._proxy.har
        requests = har['log']['entries']
        return requests

    def quit(self):
        self._server.stop()
        self._driver.quit()


