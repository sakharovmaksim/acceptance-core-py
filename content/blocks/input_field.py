from acceptance_core_py.core.actions import driver_actions
from acceptance_core_py.core.block import Block


class InputField(Block):
    def input_with_check(self, string_to_input: str, need_click_by_html: bool = False):
        """Use this method by default for 'normal' fields. It's more stability"""
        driver_actions.input_in_field(self.me, string_to_input, need_check_for_correctly_input=True,
                                      need_click_by_html=need_click_by_html)

    def input(self, string_to_input: str):
        driver_actions.input_in_field(self.me, string_to_input, need_check_for_correctly_input=False)

    def input_by_char(self, string_to_input: str, need_click_by_html: bool = False):
        driver_actions.input_in_field_by_char(self.me, string_to_input, need_click_by_html)

    def input_with_keyboard_clear(self, string_to_input: str):
        driver_actions.input_in_field(self.me, string_to_input, need_clear_field_with_keyboard=True,
                                      need_check_for_correctly_input=False)

    def grab_value_from_input_field(self) -> str:
        return driver_actions.get_attr_value_from_element(self.me, 'value')

    def clear(self):
        driver_actions.clear_field(self.me)
