import logging

from acceptance_core_py.core.actions import driver_actions
from content import content_vars
from testing_projects_common.blocks.base_block import BaseBlock
from testing_projects_common.blocks.button import Button


class HeaderMenuBlock(BaseBlock):
    block_attribute_name = content_vars.test_attr_name
    block_attribute_value = "top-line-menu"

    def get_open_men_menu_button(self) -> Button:
        return Button(
            self.me.child_by_attribute(
                content_vars.test_attr_name, "gender-men-topmenu"
            )
        )

    def click_open_men_section(self):
        logging.info("Click on men section link in header block")
        button = self.get_open_men_menu_button()
        button.wait_for_ready()
        button.click()

    def get_text(self) -> str:
        self.wait_for_ready()
        return driver_actions.grab_text_from_element(self.me)
