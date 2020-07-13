from acceptance_core_py.core.actions import driver_actions
from acceptance_core_py.core.asserts import assert_strings_pattern
from content.openers.main.main_page_opener import MainPageOpener


class TestSampleMobileClass:
    def test_mobile_simple_example_1(self):
        """Example of page opener test with capture screenshot"""
        mobile_main_page = MainPageOpener().open_mobile_main_page()
        driver_actions.add_cookie_to_domain("hide_popups", "true")

        title_text = mobile_main_page.title_block.get_title_text()
        assert_strings_pattern(needle="Бутик", haystack=title_text, comment_message="Title is not valid")
