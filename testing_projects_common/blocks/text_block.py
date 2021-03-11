from acceptance_core_py.core.actions import driver_actions
from testing_projects_common.blocks.base_block import BaseBlock


class TextBlock(BaseBlock):
    """Любой блок, внутри которого текст. Например: h1-h6, span, div"""

    def grab_text_from_element(self) -> str:
        return driver_actions.grab_text_from_element(self.me)
