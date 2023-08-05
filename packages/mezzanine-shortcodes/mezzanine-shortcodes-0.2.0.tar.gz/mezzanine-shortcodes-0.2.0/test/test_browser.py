import re
import sys
import time
import inspect
import tempfile
import unittest
import contextlib

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium.webdriver.common.keys import Keys
import splinter

from shortcodes.utils import ShortcodeSoup

from example_app.models import FeaturefulButton

import testutils


DEBUG = '--debug' in sys.argv

drivers = ['phantomjs', 'firefox', 'chrome']
try:
    WEBDRIVER = set(drivers).intersection(sys.argv).pop()
except KeyError:
    WEBDRIVER = 'phantomjs'


class SplinterTestCase(StaticLiveServerTestCase):
    def setUp(self):
        # XXX All of this could be done in setUpClass if django didn't reset
        # the database and cookies on every test.

        # XXX Seems like LiveServerTestCase ought to take care of this.
        from django.contrib.sites.models import Site
        site = Site.objects.get_current()
        site.domain = site.name = self.live_server_url.replace('http://', '')
        site.save()

        from django.contrib.auth.models import User
        User.objects.create_superuser('admin', 'admin@example.com', 'default')

        self.visit_relativeurl('/admin/login')
        self.browser.fill('username', 'admin')
        self.browser.fill('password', 'default')
        self.browser.find_by_value('Log in').click()

        self.visit_relativeurl('/admin/pages/richtextpage/add')

    @classmethod
    def setUpClass(cls):
        kwargs = {}

        if WEBDRIVER == 'phantomjs':
            # XXX Might add '--remote-debugger-port=9000' but throws exception.
            kwargs['service_args'] = [
                '--webdriver-loglevel=DEBUG'] if DEBUG else []

        try:
            cls.browser = splinter.Browser(WEBDRIVER, **kwargs)
        except splinter.exceptions.DriverNotFoundError:
            cls.browser = splinter.Browser('firefox')

        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    @property
    def messagelist(self):
        return [elem.text for elem in
                self.browser.find_by_css('.messagelist > li')]

    @property
    def source(self):
        self.browser.find_by_css('.mce-i-code').first.click()
        source = self.browser.find_by_css('textarea.mce-textbox').first.value
        self.browser.execute_script(
            "jQuery(\"button:contains('Cancel')\").click()")
        return source

    def assertInMessagelist(self, regex):
        self.assertTrue(re.search(regex, '\n'.join(self.messagelist)))

    @contextlib.contextmanager
    def assertDeletesInstance(self, model):
        initial_count = model.objects.count()
        yield
        self.assertEqual(initial_count-1, model.objects.count())

    def visit_relativeurl(self, relativeurl):
        # This can be a classmethod in django 1.9:
        # https://code.djangoproject.com/ticket/24965
        self.browser.visit(self.live_server_url + relativeurl)

    def jQueryIframe(self, ascendant_selector, method):
        # XXX Better to use splinter's get_iframe but I haven't found a way to
        # assign name or id to the iframe.
        return self.browser.evaluate_script(
            "jQuery('{selector} iframe').contents(){method}".format(
                selector=ascendant_selector, method=method))

    def jQueryDialog(self, method):
        return self.jQueryIframe('.mce-container-body.mce-abs-layout', method)

    def jQueryContent(self, method):
        return self.jQueryIframe('.mce-edit-area', method)

    def clickInsert(self):
        if WEBDRIVER == 'phantomjs':
            self.browser.execute_script(
                "jQuery(\"button:contains('Insert')\").click()")
        else:
            # XXX Doesn't work on phantomjs.
            self.browser.find_by_text('Insert').first.click()

    def insertFeaturefulButton(self):
        self.browser.find_by_text('Featureful Button').first.click()
        self.fillPerson('Spongebob')
        self.clickInsert()

    def savePage(self):
        self.browser.fill('title', 'Some Page')
        self.browser.find_by_value('Save and continue editing').click()
        time.sleep(5)  # XXX
        self.browser.is_element_present_by_css('.messagelist > .success')
        self.assertInMessagelist(
            'The Rich text page "Some Page" was (added|changed) successfully.')

    def fillPerson(self, person):
        self.jQueryDialog(
            ".find('#id_entity').val('{person}')".format(person=person))

    def debug(self, _callable):
        """
        Capture screen and html before executing the callable.

        WARNING: Taking a screenshot can cause phantomjs tests to pass.
        """
        # Introspect. Adapted from http://stackoverflow.com/a/8856387/1938621.
        caller_frame = inspect.currentframe().f_back
        frame_info = inspect.getframeinfo(caller_frame)

        lineno = frame_info.lineno

        lines = ''.join([line.strip() for line in frame_info.code_context])
        line = re.search(r'debug\((.+?)\)$', lines).group(1)

        # Capture screen and html.
        filename = '-'.join([str(lineno), line, WEBDRIVER.upper()])

        self.browser.screenshot(name=filename)

        with tempfile.NamedTemporaryFile(
                prefix=filename, suffix='.html', delete=False) as f:
            f.write(self.browser.html.encode('utf-8'))

        # Call callable.
        _callable()


class TestAdmin(SplinterTestCase):

    def test_featureful_button(self):
        button = self.browser.find_by_text('Featureful Button').first

        # Test tooltip.
        # XXX One of these higher-level API's ought to work.
        # button.mouse_over()
        # self.browser.execute_script(
        #     "jQuery('button:contains(\"Featureful Button\")').mouseover();")
        # self.browser.execute_script("""\
        #     jQuery('button:contains(\"Featureful Button\")')
        #       .trigger('mouseover');""")
        if WEBDRIVER == 'phantomjs':
            # XXX document.createEvent/initMouseEvent are deprecated
            self.browser.execute_script("""\
                var mouseover = document.createEvent('MouseEvent');
                mouseover.initMouseEvent('mouseover', canBubble=true);

                jQuery("button:contains('Featureful Button')")[0]
                  .dispatchEvent(mouseover);""")
        else:
            # XXX https://github.com/ariya/phantomjs/issues/11289
            self.browser.execute_script("""\
                jQuery("button:contains('Featureful Button')")[0]
                  .dispatchEvent(new MouseEvent('mouseover', {bubbles: true}))
            """)
        self.assertTrue(self.browser.find_by_text('Click me.').first.visible)

        # Open dialog.
        button.click()

        # Submitting with required fields empty should fail and display errors.
        self.assertFalse(self.jQueryDialog("""\
            .find(":contains('Please correct the errors below.')").toArray();
            """))
        self.clickInsert()
        time.sleep(10)  # XXX
        self.assertTrue(self.jQueryDialog("""\
            .find(":contains('Please correct the errors below.')").toArray();
            """))

        # Submit dialog.
        self.fillPerson('Spongebob')
        self.clickInsert()
        time.sleep(1)

        # Check source code.
        shortcode = ShortcodeSoup(self.source).find_shortcodes().pop()
        self.assertTrue(shortcode.has_attr('data-pending'))
        self.assertFalse(shortcode.has_attr('data-pk'))

        # Save page.
        self.savePage()

        # Check source code.
        shortcode = ShortcodeSoup(self.source).find_shortcodes().pop()
        self.assertEqual(shortcode.text, 'Featureful Button')
        self.assertEqual(shortcode['class'], ['mezzanine-shortcodes'])
        self.assertEqual(shortcode['data-name'], 'featureful_button')
        self.assertIsInstance(int(shortcode['data-pk']), int)
        self.assertEqual(shortcode['contenteditable'], 'false')
        self.assertEqual(
            set(shortcode.attrs.keys()),
            set(('class', 'contenteditable', 'data-pk', 'data-name')))

    @unittest.skipIf(WEBDRIVER == 'phantomjs', "Can't open contextmenu.")
    def test_editing(self):
        # Setup
        self.insertFeaturefulButton()
        self.savePage()

        # Open edit dialog.
        with self.browser.get_iframe('id_content_ifr') as iframe:
            shortcode = iframe.find_by_css('.mezzanine-shortcodes').first
            shortcode.click()  # XXX Shouldn't need to do this.
            if WEBDRIVER == 'phantomjs':
                # XXX raises NotImplementedError
                #  shortcode.right_click()
                # XXX doesn't work
                #  shortcode.action_chains.context_click(shortcode._element)
                #  shortcode.action_chains.perform()
                # XXX https://github.com/ariya/phantomjs/issues/11289
                #  iframe.execute_script("""\
                    #  var element = document.getElementsByClassName(
                    #    'mezzanine-shortcodes')[0],
                        #  event = new MouseEvent('contextmenu');
                    #  element.dispatchEvent(event);""")
                # XXX raises ElementNotVisibleException
                #  iframe.execute_script("""\
                    #  var shortcode = document.getElementsByClassName(
                    #    'mezzanine-shortcodes')[0],
                        #  rightclick = document.createEvent('MouseEvent');
                    #  rightclick.initMouseEvent('contextmenu');
                    #  shortcode.dispatchEvent(rightclick)""")
                # XXX https://github.com/ariya/phantomjs/issues/11637 no help.
                #  iframe.driver.maximize_window()
                #  iframe.driver.set_window_size(1400, 1000)
                #  shortcode._element.clear()
                # XXX raises ElementNotVisibleException (works in firefox)
                # Inspired by https://github.com/n1k0/casperjs/pull/1169.
                #  iframe.execute_script("""\
                    #  function computeCenter(element) {
                        #  var bounds = element.getBoundingClientRect
                        #  var x = Math.round(bounds.left + bounds.width / 2);
                        #  var y = Math.round(bounds.top  + bounds.height / 2);
                        #  return [x, y];
                    #  }

                    #  var shortcode = document.getElementsByClassName(
                    #    'mezzanine-shortcodes')[0],
                        #  rightclick = document.createEvent('MouseEvent'),
                        #  center = computeCenter(shortcode);

                    #  rightclick.initMouseEvent(
                    #    'contextmenu', true, true, window, 1,
                    #    center[0], center[1], center[0], center[1],
                    #    false, false, false, false, 2, null);
                    #  shortcode.dispatchEvent(rightclick)""")
                pass  # need to be outside iframe context to use jQuery
            else:
                shortcode.right_click()
        if WEBDRIVER == 'phantomjs':
            # XXX doesn't work
            #  self.jQueryDialog(
                #  ".find('.mezzanine-shortcodes')
                #  .triggerHandler('contextmenu')")
            # XXX doesn't work
            #  self.jQueryDialog("""\
                #  .find('.mezzanine-shortcodes')
                #  .trigger({type: 'click', which: 3});""")
            pass
        self.browser.find_by_text('Edit Shortcode').first.click()

        # Check that inputs are pre-populated.
        self.assertEqual(
            self.jQueryDialog(".find('#id_entity').val()"), 'Spongebob')

        # Modify input and submit.
        self.fillPerson('Squidward')
        self.clickInsert()
        self.savePage()

        # Open edit dialog.
        with self.browser.get_iframe('id_content_ifr') as iframe:
            shortcode = iframe.find_by_css('.mezzanine-shortcodes').first
            shortcode.click()  # XXX Shouldn't need to do this.
            shortcode.right_click()
        self.browser.find_by_text('Edit Shortcode').first.click()

        # Check that value has been modified.
        self.assertEqual(
            self.jQueryDialog(".find('#id_entity').val()"), 'Squidward')

    def test_remove_before_saving(self):
        """
        Shortcodes removed before saving the page aren't added to database.
        """
        self.insertFeaturefulButton()

        if WEBDRIVER == 'phantomjs':
            time.sleep(1)  # XXX

        # Remove shortcode.
        self.jQueryContent(".find('body').empty().append('blah')")

        # Save page.
        self.savePage()

        self.assertEqual(FeaturefulButton.objects.count(), 0)

    def test_remove_after_saving(self):
        """
        Shortcodes removed after saving the page are removed from the database.
        """
        self.insertFeaturefulButton()
        self.savePage()

        with self.assertDeletesInstance(FeaturefulButton):
            self.jQueryContent(".find('body').empty().append('blah')")
            self.savePage()

    def test_remove_after_deleting(self):
        """
        When a page is deleted, all associated shortcodes are deleted too.
        """
        self.insertFeaturefulButton()
        self.savePage()

        with self.assertDeletesInstance(FeaturefulButton):
            self.browser.find_by_text('Delete').click()
            self.browser.find_by_value("Yes, I'm sure").click()

    @unittest.skipIf(WEBDRIVER == 'phantomjs', "Can't open dialog.")
    def test_icon(self):
        self.browser.execute_script("""\
          jQuery('button > .mce-ico').filter(function() {{
            return jQuery(this).css('background-image').replace(/\"/g, '') ===
              'url({base_url}/static/img/audio.png?name=icon_button)';
          }}).click();""".format(base_url=self.live_server_url))
        self.assertTrue(self.browser.is_text_present('some button'), 5)

    def test_menu(self):
        # Test tooltip.
        # XXX One of these higher-level API's ought to work.
        # button.mouse_over()
        # self.browser.execute_script(
        #     "jQuery('button:contains(\"Featureful Button\")').mouseover();")
        # self.browser.execute_script("""\
        #     jQuery('button:contains(\"Featureful Button\")')
        #       .trigger('mouseover');""")
        if WEBDRIVER == 'phantomjs':
            # XXX document.createEvent/initMouseEvent are deprecated
            self.browser.execute_script("""\
                var mouseover = document.createEvent('MouseEvent');
                mouseover.initMouseEvent('mouseover', canBubble=true);

                jQuery('button:contains(\"Some Menu\")')[0]
                  .dispatchEvent(mouseover);""")
        else:
            # XXX https://github.com/ariya/phantomjs/issues/11289
            self.browser.execute_script("""\
                jQuery("button:contains('Some Menu')")[0]
                  .dispatchEvent(new MouseEvent('mouseover', {bubbles: true}))
            """)
        self.assertTrue(self.browser.find_by_text('Click here.').first.visible)

        # Open menu.
        self.browser.find_by_text('Some Menu').first.click()

        # Test menubutton order and display.
        buttons = self.browser.find_by_css('.mce-menu-item')
        self.assertEqual(buttons[0].value.strip(), 'some menubutton')
        self.assertEqual(buttons[1].value.strip(), 'icon menubutton')
        self.assertIn('/static/img/audio.png?name=icon_menubutton',
                      buttons[1].find_by_css('.mce-ico')['style'])
        self.assertEqual(buttons[2].value.strip(), 'generic menubutton')

        # Test genericmenubutton dialog.
        self.browser.find_by_text('generic menubutton').first.click()
        self.assertIn(
            'Prefix', self.jQueryDialog(".find('body').text()").strip())


class TestPage(SplinterTestCase):
    def test_page(self):
        # Insert Featureful Button shortcode.
        self.browser.find_by_text('Featureful Button').first.click()
        self.fillPerson('Spongebob')
        self.clickInsert()

        # Insert generic shortcode.
        if WEBDRIVER == 'phantomjs':
            self.browser.execute_script("jQuery('.mceEditor').show()")
            self.browser.find_by_css('.mceEditor').type(Keys.ENTER)

        self.browser.find_by_text('generic button model').first.click()
        self.fillPerson('Squidward')
        self.clickInsert()

        self.savePage()

        # Navigate to page.
        self.visit_relativeurl('/admin/logout/')
        self.visit_relativeurl('/some-page')

        # Test page.
        self.assertTrue(self.browser.is_text_present('Hello Spongebob!'), 5)
        self.assertTrue(self.browser.is_text_present('Hello Squidward!'), 5)

if __name__ == '__main__':
    testutils.test_module('test_browser')
