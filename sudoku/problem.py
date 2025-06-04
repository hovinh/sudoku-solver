from typing import List, Tuple, Any
import numpy as np
from sudoku.utils import constant


def has_row_divider(row_id: int) -> bool:
    return (row_id % constant.BOX_WIDTH == 0) and (row_id > 0)


def has_col_divider(col_id: int) -> bool:
    return (col_id % constant.BOX_WIDTH == 0) and (col_id > 0)


class SudokuCell(object):
    def __init__(self, row_id: int, col_id: int, value: int = 0) -> None:
        """
        Initializes SudokuCell instance.

        Parameters
        ----------
        row_id : int
            The row index of the cell on the Sudoku grid.
        col_id : int
            The column index of the cell on the Sudoku grid.
        value : int, default=0
        """
        self._row_id = row_id
        self._col_id = col_id
        if isinstance(value, int):
            self._value = value
        else:
            raise TypeError(f"Type of value is {type(value)}. Must be int.")
        self._candidates = (
            [self.value] if self.is_filled() else constant.POSSIBLE_CELL_VALUE.copy()
        )

    @property
    def value(self) -> int:
        return self._value

    @property
    def row_id(self) -> int:
        return self._row_id

    @property
    def col_id(self) -> int:
        return self._col_id

    @value.setter
    def value(self, new_value: int) -> None:
        if new_value not in constant.POSSIBLE_CELL_VALUE:
            raise ValueError(
                f"Value {new_value} is invalid. Must be in {constant.POSSIBLE_CELL_VALUE}"
            )
        self._value = new_value

    @property
    def candidates(self):
        return self._candidates

    @property
    def numb_candidates(self):
        return len(self._candidates)

    def is_filled(self):
        return self.value != constant.UNFILLED_VALUE

    @property
    def solution(self):
        return None if self.n_candidates > 1 else self.candidates[0]

    def __str__(self):
        return f"(value: {self._value}, row_id: {self._row_id}, col_id: {self._col_id})"


class SudokuSequence(object):
    def __init__(self, cells: List[Any]) -> None:
        """
        Initializes SudokuSequence instance.

        Parameters
        ----------
        cells : List[Any]
            A list of SudokuCell objects
        """
        self._cells = cells

    def __getitem__(self, index: int) -> SudokuCell:
        return self._cells[index]


class SudokuRow(SudokuSequence):
    def __init__(self, cells: List[SudokuCell]) -> None:
        """
        Initializes SudokuRow instance.

        Parameters
        ----------
        cells : List[SudokuCell]
            A list of SudokuCell objects
        """
        super().__init__(cells)

    def __str__(self):
        text_str = ""
        n_cells = len(self._cells)
        for col_id in range(n_cells):
            if has_col_divider(col_id):
                text_str += "| "
            text_str += f"{self._cells[col_id].value} "
        return text_str


class SudokuColumn(SudokuSequence):
    def __init__(self, cells: List[SudokuCell]) -> None:
        """
        Initializes SudokuColumn instance.

        Parameters
        ----------
        cells : List[SudokuCell]
            A list of SudokuCell objects
        """
        super().__init__(cells)

    def __str__(self) -> str:
        text_str = ""
        n_cells = len(self._cells)
        for row_id in range(n_cells):
            if has_row_divider(row_id):
                text_str += "-\n"
            text_str += f"{self._cells[row_id].value}\n"
        return text_str


class SudokuBox(object):
    def __init__(self, cells: List[List[SudokuCell]]) -> None:
        """
        Initializes a SudokuBox instance.

        Parameters
        ----------
        cells : List[List[SudokuCell]]
            A 2D list of SudokuCell objects representing the cells in the box.
        """
        self._cells = cells

    def __getitem__(self, index: Tuple[int, int]) -> SudokuCell:
        if isinstance(index, tuple) and len(index) == 2:
            i, j = index
            return self._cells[i, j]
        else:
            raise TypeError("Invalid index. Use obj[i, j] syntax.")

    def __str__(self):
        text_str = ""
        for row_id in range(constant.BOX_WIDTH):
            row_cells = self._cells[row_id, :]
            text_str += " ".join([f"{cell}" for cell in row_cells]) + "\n"
        return text_str


class SudokuProblem(object):
    def __init__(self, sudoku_string: str) -> None:
        """
        Initializes SudokuProblem instance.

        Parameters
        ----------
        sudoku_string : str
            A string of length 81 containing the Sudoku puzzle to be solved.
            The string should be a flat representation of the Sudoku grid,
            with each character representing the value of the cell in the
            order of row-major order.

        Returns
        -------
        None
        """
        self.grid = self.__setup_grid(sudoku_string)
        self.rows = self.__setup_rows()
        self.cols = self.__setup_cols()
        self.boxes = self.__setup_boxes()

    def __setup_grid(self, sudoku_string: str):
        str_id = 0
        grid = list()
        for row_id in range(constant.N_ROWS):
            row = list()
            for col_id in range(constant.N_COLUMNS):
                cell_value = int(sudoku_string[str_id])
                cell = SudokuCell(row_id, col_id, cell_value)
                row.append(cell)
                str_id += 1
            grid.append(row)
        return np.array(grid)

    def __setup_rows(self) -> np.array:
        rows = np.array(
            [SudokuRow(self.grid[row_id, :]) for row_id in range(constant.N_ROWS)]
        )
        return rows

    def __setup_cols(self) -> np.array:
        cols = np.array(
            [SudokuColumn(self.grid[:, col_id]) for col_id in range(constant.N_COLUMNS)]
        )
        return cols

    def __setup_boxes(self) -> np.array:
        boxes = list()
        for box_id in range(constant.N_BOXES):
            start_row_id = (box_id // constant.BOX_WIDTH) * constant.BOX_WIDTH
            end_row_id = start_row_id + 3
            start_col_id = (box_id % constant.BOX_WIDTH) * constant.BOX_WIDTH
            end_col_id = start_col_id + 3
            box = SudokuBox(self.grid[start_row_id:end_row_id, start_col_id:end_col_id])
            boxes.append(box)
        return boxes

    def __str__(self) -> str:
        text_str = ""
        last_col_id = 8
        for row_id in range(constant.N_ROWS):
            if has_row_divider(row_id):
                text_str += constant.ROW_DIVIDER

            for col_id in range(constant.N_COLUMNS):
                if has_col_divider(col_id):
                    text_str += "| "
                cell = self.grid[row_id, col_id]
                if col_id == last_col_id:
                    text_str += f"{cell.value} \n"
                else:
                    text_str += f"{cell.value} "

        return text_str

    def __getitem__(self, index: Tuple[int, int]) -> SudokuCell:
        if isinstance(index, tuple) and len(index) == 2:
            i, j = index
            return self.grid[i, j]
        else:
            raise TypeError("Invalid index. Use obj[i, j] syntax.")
