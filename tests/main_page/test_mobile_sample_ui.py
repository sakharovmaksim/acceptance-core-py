import pytest

from acceptance_core_py.core.actions import driver_actions
from acceptance_core_py.core.asserts import assert_not_equal
from content.pages.main.main_page_mobile import MainPageMobile
from content.url_builders.main.main_page_url_builder import MainPageUrlBuilder


@pytest.mark.mobile
class TestSampleMobileClass:
    def test_mobile_simple_example_1(self):
        """Example of mobile page test"""
        mobile_main_page = MainPageMobile().open_me(MainPageUrlBuilder())
        driver_actions.add_cookie_to_domain("hide_popups", "true")

        header_cart_text = mobile_main_page.header_cart_block.get_text()
        assert_not_equal(
            "bad cart", header_cart_text, "Header Cart text must be not empty"
        )
