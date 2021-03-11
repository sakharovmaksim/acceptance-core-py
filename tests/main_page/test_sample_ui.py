from acceptance_core_py.core.actions import driver_actions
from acceptance_core_py.core.asserts import assert_not_equal
from acceptance_core_py.core.asserts import assert_selector_exists
from acceptance_core_py.core.asserts import assert_selector_visible
from acceptance_core_py.core.asserts import assert_strings_pattern
from content.pages.main.main_page import MainPage
from content.url_builders.main.main_page_url_builder import MainPageUrlBuilder


class TestSampleClass:
    def test_simple_example_1(self):
        """Example of desktop page test"""
        main_page = MainPage().open_me(MainPageUrlBuilder())
        driver_actions.add_cookie_to_domain("hide_popups", "true")
        header_menu_block = main_page.header_menu_block
        assert_selector_visible(header_menu_block.me, "Header block is not visible")

        menu_text = header_menu_block.get_text()
        assert_strings_pattern(
            needle="женщинам",
            haystack=menu_text,
            comment_message="Menu text is not valid",
        )

    def test_simple_example_2(self):
        """Example of test with Page -> Block mechanics"""
        main_page = MainPage().open_me(MainPageUrlBuilder())
        main_page = main_page.click_men_section_and_open_main_page()

        header_menu_block = main_page.header_menu_block
        assert_selector_exists(header_menu_block.me, "Header block is not exists")

        menu_text = header_menu_block.get_text()
        assert_strings_pattern(
            needle="женщинам",
            haystack=menu_text,
            comment_message="Menu text is not valid",
        )

    def test_simple_example_3(self):
        main_page = MainPage().open_me(MainPageUrlBuilder())
        menu_text = main_page.header_menu_block.get_text()
        assert_not_equal("", menu_text, "Title can't be empty!")

    def test_simple_example_4(self):
        main_page = MainPage().open_me(MainPageUrlBuilder())
        menu_text = main_page.header_menu_block.get_text()
        # Sample of direct Python assert
        assert menu_text != "", "Title can't be empty!"
