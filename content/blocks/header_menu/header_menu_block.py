from acceptance_core_py.core.block import Block
from content import content_variables


class HeaderMenuBlock(Block):
    block_attribute_name = content_variables.test_attr_name
    block_attribute_value = "top-line-menu"
