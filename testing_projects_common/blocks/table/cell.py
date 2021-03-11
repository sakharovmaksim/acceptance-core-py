from acceptance_core_py.core.actions import driver_actions
from testing_projects_common.blocks.base_block import BaseBlock


class Cell(BaseBlock):
    """Ячейка таблицы"""

    def get_text(self) -> str:
        return driver_actions.grab_text_from_element(self.me)

    def click(self):
        driver_actions.click(self.me)
