# -*- encoding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
import time
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, InvalidSelectorException, NoSuchElementException
from monitio import ERROR, notify, INFO
from monitio.models import Monit

from selenium_helpers import SeleniumTestCase, wd, MyWebDriver

User = get_user_model()


class IndexPageMixin:
    def close_all_div(self):
        return self.find_element_by_jquery(".message-close-all-div")

    def close_all_link(self):
        return self.find_element_by_jquery(".message-close-all")

    def message_div(self, message_id):
        return self.find_element_by_jquery("#message-%i" % message_id)

    def add_message_by_js(self, pk, subject, message):
        return self.execute_script("""newMessage({'pk':arguments[0],
            'subject': arguments[1], 'message': arguments[2]});""",
                                   pk, subject, message)


class IndexPageFirefox(IndexPageMixin, MyWebDriver(webdriver.Firefox)):
    pass


class IndexPageChrome(IndexPageMixin, MyWebDriver(webdriver.Chrome)):
    pass


class IndexPageIe(IndexPageMixin, MyWebDriver(webdriver.Ie)):
    pass


class MonitioTestCase(SeleniumTestCase):
    url = reverse('index') + "?no_sse=1"
    pageClass = IndexPageFirefox

    def assertCloseAllVisible(self):
        self.assertEquals(self.page.close_all_div().visible(), True)

    def assertCloseAllInvisible(self):
        self.assertEquals(self.page.close_all_div().visible(), False)

    def setUp(self):
        SeleniumTestCase.setUp(self)

        u = User.objects.create_superuser('foo', 'foo@foo.pl', 'bar')
        self.login_via_admin(u.username, 'bar', then=self.url)
        self.user = u


class TestSeleniumLoggedIn(MonitioTestCase):
    def test_index(self):
        pass

    def test_no_messages(self):
        print self.page.page_source
        self.assertCloseAllInvisible()

    def test_add_message_by_js(self):
        self.assertCloseAllInvisible()

        self.page.add_message_by_js(1, "foo", "bar")
        self.assertCloseAllInvisible()

        self.page.add_message_by_js(2, "foo", "bar")
        self.assertCloseAllVisible()

    def create_messages(self, no):
        for a in range(no):
            x = Monit.objects.create(message='LOL 123', level=ERROR,
                                     user=self.user)
        return x

    def test_closeall_single_message(self):
        self.assertCloseAllInvisible()
        self.create_messages(1)
        self.reload()
        self.assertCloseAllInvisible()

    def test_closeall_bug(self):
        self.assertCloseAllInvisible()

        x = self.create_messages(3)
        self.reload()

        self.assertIn("LOL 123", self.page.page_source)
        self.assertCloseAllVisible()

        self.page.close_all_link().click()
        time.sleep(2)
        # Div was removed
        try:
            self.assertRaises(StaleElementReferenceException,
                              self.page.message_div, x.pk)
        except InvalidSelectorException:
            # This one is OK, too
            pass

        # Let's try adding a message by hand:
        # ... and this will fail, because there is a BUG TO FIX!
        self.page.add_message_by_js(1, "foo", "bar")
        # Is it fixed?
        self.assertCloseAllInvisible()
        # For real?
        self.page.add_message_by_js(2, "foo", "bar")
        time.sleep(2)
        # Looks like it...
        self.assertCloseAllVisible()
        # Whew! Let's try that again:

        self.page.close_all_link().click()
        time.sleep(1)
        self.assertCloseAllInvisible()
        self.page.add_message_by_js(1, "foo", "bar")
        self.assertCloseAllInvisible()
        self.page.add_message_by_js(2, "foo", "bar")
        self.assertCloseAllVisible()


class SimpleEventsourceMixin:
    url = reverse('index')

    def test_index(self):
        from monitio.conf import settings
        print settings.TESTING

        time.sleep(2)

        notify.sse(
            INFO, 31337, 'WUTLOLSKI', 'info unread', "Subject", 'foo', 'foo')

        self.assertRaises(NoSuchElementException,
                          self.page.find_element_by_id,
                          "#message-31337")

        time.sleep(2)

        self.page.find_element_by_id("message-31337")


class TestEventsourceFirefox(SimpleEventsourceMixin, MonitioTestCase):
    pageClass = IndexPageFirefox


class TestEventsourceChrome(SimpleEventsourceMixin, MonitioTestCase):
    pageClass = IndexPageChrome


# This fails to open the web page and I don't know why
# class TestEventsourceIe(SimpleEventsourceMixin, MonitioTestCase):
#     pageClass = IndexPageIe