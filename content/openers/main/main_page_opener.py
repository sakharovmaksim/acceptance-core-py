from acceptance_core_py.core.actions import driver_actions
from content.pages.main.main_page import MainPage
from content.pages.main.mobile_main_page import MobileMainPage


class MainPageOpener:
    def open_main_page(self) -> MainPage:
        driver_actions.open_relative_url_using_base_url()
        main_page = MainPage()
        main_page.wait_for_ready()
        return main_page

    def open_mobile_main_page(self) -> MobileMainPage:
        driver_actions.open_relative_url_using_base_url()
        mobile_main_page = MobileMainPage()
        mobile_main_page.wait_for_ready()
        return mobile_main_page
