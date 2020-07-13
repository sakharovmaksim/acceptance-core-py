from acceptance_core_py.core.actions import driver_actions
from acceptance_core_py.core.asserts import assert_selector_visible, assert_strings_pattern, assert_selector_exists, \
    assert_not_equal
from content.openers.main.main_page_opener import MainPageOpener


class TestSampleClass:
    def test_simple_example_1(self):
        """Example of page opener test with capture screenshot"""
        main_page = MainPageOpener().open_main_page()
        driver_actions.add_cookie_to_domain("hide_popups", "true")

        title_text = main_page.title_block.get_title_text()

        assert_strings_pattern(needle="Бутик", haystack=title_text, comment_message="Title is not valid")
        assert_selector_visible(
            main_page.header_menu_block.me, "Header block is not visible")

    def test_simple_example_2(self):
        """Example of test with Page -> Block mechanics"""
        main_page = MainPageOpener().open_main_page()
        main_page = main_page.click_men_section_and_open_main_page()
        title_text = main_page.title_block.get_title_text()
        assert_strings_pattern(needle="Бутик", haystack=title_text, comment_message="Title is not valid")

        header_block = main_page.header_menu_block
        assert_selector_exists(header_block.me, "Header block is not exists")
        assert_not_equal(expected="", actual=header_block.get_text_from_main_menu(),
                         comment_message="Main menu text must be not empty")

    def test_simple_example_3(self):
        main_page = MainPageOpener().open_main_page()
        title_text = main_page.title_block.get_title_text()
        assert_not_equal("", title_text, "Title can't be empty!")

    def test_simple_example_4(self):
        main_page = MainPageOpener().open_main_page()
        title_text = main_page.title_block.get_title_text()
        # Sample of direct Python assert
        assert title_text != "", "Title can't be empty!"
