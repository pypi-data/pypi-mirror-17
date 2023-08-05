from __future__ import unicode_literals
import os
import tempfile
import sys
import codecs
import pickle
import logging
import time
from contextlib import contextmanager
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, \
    WebDriverException, \
    NoSuchWindowException
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
from bs4 import Tag

from selenium.webdriver.firefox.webdriver import WebDriver as BaseWebDriver
#from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.firefox.webelement import FirefoxWebElement as BaseWebElement # selenium 3.0
#from selenium.webdriver.remote.webelement import WebElement as BaseWebElement # selenium <3.0

from .compat import *


logger = logging.getLogger(__name__)


class ParseError(RuntimeError):
    """This gets raised any time Browser.element() fails to parse,
    it wraps NoSuchElementException"""
    def __init__(self, body, e):
        self.body = body
        self.error = e
        super(ParseError, self).__init__(e.message)


class RecoverableCrash(IOError):
    def __init__(self, e):
        self.error = e
        super(RecoverableCrash, self).__init__(e.message)


class Soup(object):
    def soupify(self, body):
        if isinstance(body, Tag): return body
        soup = BeautifulSoup(body, "html.parser")
        return soup


# class WebElement(BaseWebElement):
#     @property
#     def body(self):
#         """Return the body of this particular element"""
#         # http://stackoverflow.com/a/22227980/5006
#         return self.get_attribute('innerHTML')
# 
#     @property
#     def soup(self):
#         """Return a beautiful soup object with the contents of this element"""
#         soup = getattr(self, "_soup", None)
#         if soup is None:
#             soup = BeautifulSoup(self.body, "html.parser")
#             self._soup = soup
#         return soup
# 
# 
# class WebDriver(BaseWebDriver):
#     _web_element_cls = WebElement # selenium 3.0
# 
#     def create_web_element(self, element_id):
#         # TODO -- remove when upgrading to selenium 3.0
#         return WebElement(self, element_id, w3c=self.w3c)


class Cookies(object):
    """This will write and read cookies for a Browser instance, calling Browser.location()
    will use this class to load cookies for the given domain if they are available"""
    @property
    def directory(self):
        directory = getattr(self, "_directory", None)
        if directory is None:
            directory = os.environ.get("BROWSER_CACHE_DIR", "")
            if directory:
                directory = os.path.abspath(os.path.expanduser(directory))
            else:
                directory = tempfile.gettempdir()

            self._directory = directory
        return directory

    @property
    def path(self):
        cookies_d = self.directory
        cookies_f = os.path.join(cookies_d, "{}.txt".format(self.domain))
        return cookies_f

    def __iter__(self):
        cookies_f = self.path
        if os.path.isfile(cookies_f):
            with open(cookies_f, "rb") as f:
                cookies = pickle.load(f)

            for cookie in cookies:
                yield cookie

    def save(self, cookies):
        """save the cookies in browser"""
        cookies_f = self.path
        with open(cookies_f, "w+b") as f:
            pickle.dump(cookies, f)

    def __init__(self, domain):
        """
        browser -- selenium web driver -- usually Firefox or Chrome
        """
        self.domain = domain


class Browser(Soup):
    """This is a wrapper around selenium and pyvirtualdisplay to make browsering
    from the command line easier

    link -- Selinium source -- https://github.com/SeleniumHQ/selenium/tree/master/py
    """
    @property
    def body(self):
        """return the body of the current page"""
        # http://stackoverflow.com/a/7866938/5006
        return self.browser.page_source

    @property
    def current_url(self):
        """return the current url"""
        # http://stackoverflow.com/questions/15985339/how-do-i-get-current-url-in-selenium-webdriver-2-python
        return self.browser.current_url

    @property
    def browser(self):
        """wrapper around the browser in case we want to switch from Firefox, you
        should use this over the .firefox property"""
        browser = getattr(self, "_browser", None)
        if browser is None:
            browser = self.chrome
            #browser._web_element_cls = WebElement
            self._browser = browser

        return browser

    @browser.deleter
    def browser(self):
        try:
            self._browser.close()
            del self._browser
        except (WebDriverException, AttributeError):
            pass

    @property
    def display(self):
        display = getattr(self, "_display", None)
        if display is None:
            # http://coreygoldberg.blogspot.com/2011/06/python-headless-selenium-webdriver.html
            display = Display(visible=0, size=(800, 600))
            display.start()
            self._display = display
        return display

    @property
    def chrome(self):
        chrome = webdriver.Chrome()
        return chrome

#     @property
#     def firefox(self):
#         profile = webdriver.FirefoxProfile()
#         #firefox = webdriver.Firefox(firefox_profile=profile)
#         firefox = WebDriver(firefox_profile=profile)
#         return firefox


    @classmethod
    @contextmanager
    def open(cls):
        """Where all the magic happens, you use this to start the virtual display
        and power up the browser

        with Browser.open() as browser:
            browser.location("http://example.com")
        """
        try:
            instance = cls()
            # start up the display
            instance.display
            yield instance

        except WebDriverException as e:
            logger.exception(e)
            del instance.browser
            raise RecoverableCrash(e)

        except Exception as e:
            logger.exception(e)
            exc_info = sys.exc_info()

            if instance:
                try:
                    directory = tempfile.gettempdir()
                    filename = os.path.join(directory, "wishlist.png")
                    instance.browser.get_screenshot_as_file(filename)
                except Exception as e:
                    pass

                try:
                    with codecs.open(os.path.join(directory, "wishlist.html"), encoding='utf-8', mode='w+') as f:
                        f.write(instance.body)
                except Exception as e:
                    pass

            reraise(*exc_info)

        finally:
            instance.close()






    # DEPRECATED 9-7-2016, use open() instead
    @classmethod
    @contextmanager
    def lifecycle(cls):
        """Where all the magic happens, you use this to start the virtual display
        and power up the browser

        with Browser.lifecycle() as browser:
            browser.location("http://example.com")
        """
        try:
            instance = cls()
            # start up the display
            instance.display
            yield instance

        except Exception as e:
            logger.exception(e)
            exc_info = sys.exc_info()

            if instance:
                try:
                    directory = tempfile.gettempdir()
                    filename = os.path.join(directory, "wishlist.png")
                    instance.browser.get_screenshot_as_file(filename)
                except Exception as e:
                    pass

                try:
                    with codecs.open(os.path.join(directory, "wishlist.html"), encoding='utf-8', mode='w+') as f:
                        f.write(instance.body)
                except Exception as e:
                    pass

            reraise(*exc_info)

        finally:
            instance.close()

    def location(self, url, ignore_cookies=False):
        """calls the selenium driver's .get() method, and will load cookies if they
        are available

        url -- string -- the full url (scheme, domain, path)
        ignore_cookies -- boolean -- if True then don't try and load cookies
        """
        logger.debug("Loading location {}".format(url))
        driver = self.browser
        driver.get(url)
        url_bits = urlparse.urlparse(url)
        domain = url_bits.hostname
        self.domain = domain

        if not ignore_cookies:
            if domain and (domain not in self.domains):
                logger.debug("Loading cookies for {}".format(domain))
                self.domains[domain] = domain
                cookies = Cookies(domain)
                count = 0
                for count, cookie in enumerate(cookies, 1):
                    driver.add_cookie(cookie)
                logger.debug("Loaded {} cookies".format(count))

    def element_exists(self, css_selector):
        ret = True
        try:
            self.browser.find_element_by_css_selector(css_selector)
        except NoSuchElementException as e:
            ret = False
        return ret

    def element(self, css_selector):
        """wrapper around Selenium's css selector that raises ParseError if fails"""
        try:
            return self.browser.find_element_by_css_selector(css_selector)

        except NoSuchElementException as e:
            logger.exception(e)
            raise ParseError(self.body, e)

    def wait_for_element(self, css_selector, seconds):
        # ??? -- not sure this is needed or is better than builtin methods
        elem = None
        driver = self.browser
        for count in range(seconds):
            elem = driver.find_element_by_css_selector(css_selector)
            if elem:
                break
            else:
                time.sleep(1)

        return elem


    def __init__(self):
        self.domains = {}

    def save(self):
        """save the browser session for the given domain"""
        logger.debug("Saving cookies for {}".format(self.domain))
        cookie = Cookies(self.domain)
        cookie.save(self.browser.get_cookies())

    def close(self):
        """quit the browser and power down the virtual display"""
        logger.debug("Closing down browser")
        try:
            self.browser.close()
        except Exception as e:
            logger.warn("Browser close failed with {}".format(e.message))
            pass

        logger.debug("Shutting down display")
        self.display.stop()

