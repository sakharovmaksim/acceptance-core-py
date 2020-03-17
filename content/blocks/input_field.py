from acceptance_core_py.core.actions import driver_actions
from acceptance_core_py.core.block import Block


class InputField(Block):
    def input_with_check(self, string_to_input: str):
        """Use this method by default for 'normal' fields. It's more stability"""
        driver_actions.input_in_field(self.me, string_to_input, need_check_for_correctly_input=True)

    def input(self, string_to_input: str):
        driver_actions.input_in_field(self.me, string_to_input, need_check_for_correctly_input=False)
