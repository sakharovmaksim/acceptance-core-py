from acceptance_core_py.core.actions import driver_actions
from testing_projects_common.blocks.base_block import BaseBlock


class Link(BaseBlock):
    """Любая ссылка"""

    def click(self):
        driver_actions.click(self.me)

    def click_by_html(self):
        driver_actions.click_by_html(self.me)

    def click_and_go_to_page_in_current_window(self, page, html_click: bool = False):
        self.click_by_html() if html_click else self.click()
        page.wait_for_ready()
        return page

    def click_and_go_to_page_in_next_window(self, page, html_click: bool = False):
        self.click_by_html() if html_click else self.click()
        driver_actions.switch_to_next_window()
        page.wait_for_ready()
        return page

    def get_text(self) -> str:
        return driver_actions.grab_text_from_element(self.me)

    def get_href_value(self) -> str:
        return driver_actions.get_attr_value_from_element(self.me, "href")
