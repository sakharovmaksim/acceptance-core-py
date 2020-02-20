from acceptance_core_py.core.test_case import TestCase, decorator_screenshot_on_failed_test
from content.openers.main.main_page_opener import MainPageOpener
from acceptance_core_py.core.actions.screenshot_actions import ScreenshotActions


class TestClass(TestCase):
    @decorator_screenshot_on_failed_test
    def test_simple_example_1(self):
        """Example of page opener test with capture screenshot"""
        main_page = MainPageOpener().open_main_page()
        title_text = main_page.title_block.get_title_text()

        self.assert_strings_pattern(needle="Бутик", haystack=title_text, comment_message="Title is not valid")
        self.assert_selector_visible(
            main_page.header_menu_block.me.__str__(), "Header block is not visible")
        ScreenshotActions.get_instance().capture_screenshot()

    @decorator_screenshot_on_failed_test
    def test_simple_example_2(self):
        """Example of test with Page -> Block mechanics"""
        main_page = MainPageOpener().open_main_page()
        main_page = main_page.click_men_section_and_open_main_page()
        title_text = main_page.title_block.get_title_text()
        self.assert_strings_pattern(needle="Бутик", haystack=title_text, comment_message="Title is not valid")

        header_block = main_page.header_menu_block
        self.assert_selector_exists(header_block.me.__str__(), "Header block is not exists")
        self.assert_not_equal(expected="", actual=header_block.get_text_from_main_menu(),
                              comment_message="Main menu text must be not empty")

    @decorator_screenshot_on_failed_test
    def test_simple_example_3(self):
        main_page = MainPageOpener().open_main_page()
        title_text = main_page.title_block.get_title_text()
        self.assert_not_equal("", title_text, "Title can't be empty!")

    @decorator_screenshot_on_failed_test
    def test_simple_example_4(self):
        main_page = MainPageOpener().open_main_page()
        title_text = main_page.title_block.get_title_text()
        # Sample of direct Python assert
        assert title_text != "", "Title can't be empty!"
