from acceptance_core_py.core.actions import driver_actions
from acceptance_core_py.core.exception.at_exception import ATException
from acceptance_core_py.core.selector import Selector
from acceptance_core_py.helpers.utils.collections_utils import (
    check_collection_is_not_empty,
)
from acceptance_core_py.helpers.utils.collections_utils import is_exist_index_in_list
from testing_projects_common.blocks.base_block import BaseBlock
from testing_projects_common.blocks.table.cell import Cell


class Row(BaseBlock):
    """Строка таблицы"""

    def __get_cell_selector(self) -> Selector:
        return self.me.child_by_tag("td", False)

    def get_all_cells_in_row(self) -> list[Cell]:
        cells = list()
        cells_count = driver_actions.get_elements_count(self.__get_cell_selector())

        for cell_index, _ in enumerate(range(cells_count), 1):
            cell = self.__get_cell_selector().nth_of_type(cell_index)
            if driver_actions.is_element_exists(cell):
                cells.append(Cell(cell))

        return cells

    def get_first_cell(self) -> Cell | None:
        cells = self.get_all_cells_in_row()
        check_collection_is_not_empty(cells, f"Empty collection {cells=}")
        return cells[0]

    def get_last_cell(self) -> Cell | None:
        cells = self.get_all_cells_in_row()
        check_collection_is_not_empty(cells, f"Empty collection {cells=}")
        return cells[-1]

    def get_cell_by_index(self, index: int) -> Cell | None:
        cells = self.get_all_cells_in_row()
        if not is_exist_index_in_list(cells, index):
            raise ATException(f"Not exist {index=} in {cells=}")
        return cells[index]
