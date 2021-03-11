from acceptance_core_py.core.actions import driver_actions
from content import content_vars
from testing_projects_common.blocks.base_block import BaseBlock


class HeaderCartBlock(BaseBlock):
    block_attribute_name = content_vars.test_attr_name
    block_attribute_value = "mobile-header-cart"

    def get_text(self) -> str:
        return driver_actions.grab_text_from_element(self.me)
