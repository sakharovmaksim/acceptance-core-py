from acceptance_core_py.core.actions import driver_actions
from acceptance_core_py.core.exception.at_exception import ATException
from acceptance_core_py.core.selector import Selector
from acceptance_core_py.helpers.utils.collections_utils import is_exist_index_in_list
from testing_projects_common.blocks.base_block import BaseBlock
from testing_projects_common.blocks.table.cell import Cell
from testing_projects_common.blocks.table.row import Row


class Table(BaseBlock):
    """Любая стандартно-сверстанная таблица"""

    def get_row_selector(self) -> Selector:
        return self.me.child_by_tag("tr", False)

    def get_rows(self) -> list[Row]:
        """Возвращает list, в котором все строки таблицы"""
        rows = list()
        rows_count = driver_actions.get_elements_count(self.get_row_selector())

        for row_index, _ in enumerate(range(rows_count), 1):
            row = self.get_row_selector().nth_of_type(row_index)
            if driver_actions.is_element_exists(row):
                rows.append(Row(row))

        return rows

    def get_row_by_index(self, row_number: int) -> Row:
        """Получаем строку по указанному номеру из таблицы"""
        rows = self.get_rows()
        if not is_exist_index_in_list(rows, row_number):
            raise ATException(f"Not exist {row_number=} in {rows=}")
        return rows[row_number]

    def get_cells_by_row(self, row_number: int) -> list[Cell]:
        """Все ячейки из выбранной строки"""
        rows = self.get_rows()
        if not is_exist_index_in_list(rows, row_number):
            raise ATException(f"Not exist {row_number} in {rows}")

        row = rows[row_number]
        return row.get_all_cells_in_row()

    def get_all_cells(self) -> list[Cell]:
        """Все ячейки таблицы"""
        cells = list()
        rows = self.get_rows()

        for row in rows:
            cells += row.get_all_cells_in_row()

        return cells

    def get_cells_by_coll(self, coll_number: int) -> list[Cell]:
        """Все ячейки указанного столбца"""
        cells_in_coll = list()
        rows = self.get_rows()

        for row in rows:
            cell = row.get_cell_by_index(coll_number)
            cells_in_coll.append(cell)

        return cells_in_coll

    def get_cells_by_first_coll(self) -> list[Cell]:
        """Все ячейки первого столбца"""
        cells_in_coll = list()
        rows = self.get_rows()

        for row in rows:
            cell = row.get_first_cell()
            cells_in_coll.append(cell)

        return cells_in_coll

    def get_cells_by_last_coll(self) -> list[Cell]:
        """Все ячейки последнего столбца"""
        cells_in_coll = list()
        rows = self.get_rows()

        for row in rows:
            cell = row.get_last_cell()
            cells_in_coll.append(cell)

        return cells_in_coll

    def get_rows_count(self) -> int:
        """Получаем количество строк во всей таблице"""
        return len(self.get_rows())
