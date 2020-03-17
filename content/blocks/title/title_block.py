from acceptance_core_py.core.actions import driver_actions
from acceptance_core_py.core.block import Block


class TitleBlock(Block):
    block_tag = "title"

    def get_title_text(self) -> str:
        return driver_actions.grab_text_from_element(self.me)
