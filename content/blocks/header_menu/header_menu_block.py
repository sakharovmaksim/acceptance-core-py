import logging

from acceptance_core_py.core.block import Block
from content.blocks.button import Button
from content import content_vars


class HeaderMenuBlock(Block):
    block_attribute_name = content_vars.test_attr_name
    block_attribute_value = "top-line-menu"

    def get_open_men_menu_button(self) -> Button:
        return Button(self.me().child_by_attribute(content_vars.test_attr_name, "gender-men-topmenu").__str__())

    def click_open_men_section(self):
        logging.info("Click on men section link in header block")
        self.get_open_men_menu_button().click()
