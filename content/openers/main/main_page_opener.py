from acceptance_core_py.core.actions import driver_actions
from content.pages.main.main_page import MainPage


class MainPageOpener:
    def open_main_page(self) -> MainPage:
        driver_actions.open_relative_url("")
        main_page = MainPage()
        main_page.wait_for_ready()
        return main_page
