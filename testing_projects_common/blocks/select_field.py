from acceptance_core_py.core.actions import driver_actions
from testing_projects_common.blocks.base_block import BaseBlock


class SelectField(BaseBlock):
    """Любое поле с выбором какого-то значения в нем"""

    def select(self, value_to_select: str):
        driver_actions.select_by_value(self.me, value_to_select, True)
