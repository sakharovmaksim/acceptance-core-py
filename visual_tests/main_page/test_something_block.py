from content.openers.main.main_page_opener import MainPageOpener
from visual_tests.steps import visual_models_diff_step
from acceptance_core_py.core.asserts import assert_less_equal
from visual_tests.diff_percents_tolerance import default_models_tolerance


class TestTitleBlock:
    def disabled_test_title_block(self):
        """Sample of test. Enable this test when you setting up config for Cloud Storage visual models"""
        main_page = MainPageOpener().open_main_page()

        models_diff_percent = visual_models_diff_step.perform_reference_and_candidate_element_diff(
            main_page.title_block.web_element)
        if models_diff_percent is None:
            return

        assert_less_equal(models_diff_percent, default_models_tolerance,
                          f"Title block models diff must be less than {default_models_tolerance}%")
