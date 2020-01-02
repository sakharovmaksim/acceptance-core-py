"""Block of abstract button in project"""

from acceptance_core_py.core.actions import driver_actions
from acceptance_core_py.core.block import Block


class Button(Block):
    def click(self):
        driver_actions.click(self.me.__str__())

    def click_by_html(self):
        driver_actions.click_by_html(self.me.__str__())
