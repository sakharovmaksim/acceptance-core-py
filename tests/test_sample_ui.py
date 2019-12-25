from acceptance_core_py.core.actions import driver_actions
from acceptance_core_py.core.test_case import TestCase
from content.openers.main.main_page_opener import MainPageOpener


class TestClass(TestCase):
    def test_simple_test_1(self):
        main_page = MainPageOpener().open_main_page()
        title_text = main_page.get_title_block().get_title_text()
        assert title_text != "", "Title text must be not empty"
        assert driver_actions.is_element_exists(main_page.get_header_menu_block().me().__str__()), "Header block is not exists"

    def test_simple_test_2(self):
        main_page = MainPageOpener().open_main_page()
        title_text = main_page.get_title_block().get_title_text()
        assert title_text != "", "Title can't be empty!"

    def test_simple_test_3(self):
        main_page = MainPageOpener().open_main_page()
        title_text = main_page.get_title_block().get_title_text()
        assert title_text != "", "Title can't be empty!"

    def test_simple_test_4(self):
        main_page = MainPageOpener().open_main_page()
        title_text = main_page.get_title_block().get_title_text()
        assert title_text != "", "Title can't be empty!"

    def test_simple_test_5(self):
        main_page = MainPageOpener().open_main_page()
        title_text = main_page.get_title_block().get_title_text()
        assert title_text != "", "Title can't be empty!"

    def test_simple_test_6(self):
        main_page = MainPageOpener().open_main_page()
        title_text = main_page.get_title_block().get_title_text()
        assert title_text != "", "Title can't be empty!"

    def test_simple_test_7(self):
        main_page = MainPageOpener().open_main_page()
        title_text = main_page.get_title_block().get_title_text()
        assert title_text != "", "Title can't be empty!"
