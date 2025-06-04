import numpy as np
from typing import List
from sudoku.problem import SudokuProblem
from sudoku.utils import constant


class SudokuViewer(object):
    def __init__(self):
        pass

    def print(self, sudoku: SudokuProblem) -> str:
        view_array = self.render(sudoku)
        print(self.__array_to_str(view_array))

    def log(self, sudoku: SudokuProblem) -> None:
        view_array = self.render(sudoku)
        # logger.info()

    def render(self, sudoku_problem: SudokuProblem) -> np.array:
        view_array = np.array(constant.DISPLAY_TEMPLATE)
        ROW_OFFSET = 1
        COLUMN_OFFSET = 2

        for row_id in range(constant.N_ROWS):
            for col_id in range(constant.N_COLUMNS):
                sudoku_cell = sudoku_problem[row_id, col_id]
                cell_view = constant.CELL_IS_NOT_FILLED_TEMPLATE.copy()
                if sudoku_cell.is_filled():
                    cell_view[constant.FILLED_INDEX] = sudoku_cell.value
                else:
                    cell_view = np.array(
                        [
                            value if value in sudoku_cell.candidates else " "
                            for value in constant.POSSIBLE_CELL_VALUE
                        ]
                    ).reshape(3, 3)

                numb_row_dividers = row_id
                start_row_cell = ROW_OFFSET + row_id * 3 + numb_row_dividers
                numb_col_dividers = col_id + col_id // 3
                start_col_cell = COLUMN_OFFSET + col_id * 3 + numb_col_dividers
                view_array[
                    start_row_cell : start_row_cell + 3,
                    start_col_cell : start_col_cell + 3,
                ] = cell_view

        return view_array

    def __array_to_str(self, view_array: List[List[str]]) -> str:
        return "\n".join(["".join(row) for row in view_array])
