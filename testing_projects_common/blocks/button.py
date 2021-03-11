from acceptance_core_py.core.actions import driver_actions
from testing_projects_common.blocks.base_block import BaseBlock


class Button(BaseBlock):
    """Любая кнопка"""

    def click(self):
        driver_actions.click(self.me)

    def click_by_html(self):
        driver_actions.click_by_html(self.me)
