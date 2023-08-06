"""desmos2python/browser.py

Headless browser functionality
"""

from selenium import webdriver
import importlib
import importlib.resources
import importlib.util


class DesmosWebSession(object):
    """connect to (possibly remote) desmos graphs.

    ...via headless selenium-powered browser session.
    """

    desmos_url_head = 'https://www.desmos.com/calculator/'
    
    def __init__(self, url='8tb0onyoep'):
        self.url = self.format_url(url)
        self.js_string = self.get_local_js()
        self.browser = None
        self.init_browser()

    def format_url(self, url):
        if DesmosWebSession.desmos_url_head not in url:
            url = f'{DesmosWebSession.desmos_url_head}{url}'
        return url

    def init_browser(self):
        """initialize headless browser webdriver"""
        #: ref: https://pythonbasics.org/selenium-firefox-headless/
        fireFoxOptions = webdriver.FirefoxOptions()
        fireFoxOptions.headless = True
        browser = webdriver.Firefox(options=fireFoxOptions)
        browser.get(self.url)
        self.browser = browser

    def execute_js(self):
        self.browser.execute_script(self.js_string)

    @staticmethod
    def get_local_js():
        js_string = \
            importlib.resources.open_text(
                'resources.javascript',
                'get_latex_desmos.js').read()
        return js_string
