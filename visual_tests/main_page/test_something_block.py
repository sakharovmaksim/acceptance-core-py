import pytest

from content.pages.main.main_page import MainPage
from content.url_builders.main.main_page_url_builder import MainPageUrlBuilder
from visual_tests.steps import visual_models_diff_step
from acceptance_core_py.core.asserts import assert_less_equal
from visual_tests.diff_percents_tolerance import default_models_tolerance


class TestTitleBlock:
    @pytest.mark.skip(reason="Enable this test when you setting up config for Cloud Storage visual models")
    def test_header_menu_visual_block(self):
        """Sample of test. Enable this test when you setting up config for Cloud Storage visual models"""
        main_page = MainPage().open_me(MainPageUrlBuilder())

        models_diff_percent = visual_models_diff_step.perform_reference_and_candidate_element_diff(
            main_page.header_menu_block.web_element)
        if models_diff_percent is None:
            return

        assert_less_equal(models_diff_percent, default_models_tolerance,
                          f"Header menu block models diff must be less than {default_models_tolerance}%")
