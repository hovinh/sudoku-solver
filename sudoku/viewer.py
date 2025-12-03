import numpy as np
from typing import List
from sudoku.problem import SudokuProblem
from sudoku.utils import constant
from logzero import logger


class SudokuViewer(object):
    def __init__(self, sudoku: SudokuProblem) -> None:
        self.sudoku = sudoku

    def print(self) -> str:
        view_array = self.render(self.sudoku)
        print(self.__array_to_str(view_array))

    def log(self) -> None:
        view_array = self.render(self.sudoku)
        logger.info(self.__array_to_str(view_array))

    def render(self, sudoku_problem: SudokuProblem) -> np.array:
        view_array = np.array(constant.DISPLAY_TEMPLATE)
        ROW_OFFSET = 2
        COLUMN_OFFSET = 6

        for row_id in range(constant.NUMB_ROWS):
            for col_id in range(constant.NUMB_COLUMNS):
                # Get the corresponding cell in the Sudoku problem and show
                # its value or candidates (if not solved)
                sudoku_cell = sudoku_problem[row_id, col_id]
                cell_view = constant.CELL_IS_NOT_FILLED_TEMPLATE.copy()
                if sudoku_cell.is_solved():
                    cell_view[constant.FILLED_INDEX] = sudoku_cell.value
                else:
                    # Extract candidates to show in the cell view
                    cell_view = np.array(
                        [
                            value if value in sudoku_cell.candidates else " "
                            for value in constant.DEFAULT_POSSIBLE_CELL_VALUE
                        ]
                    ).reshape(3, 3)

                # Calculate the starting position to place the cell view in the overall view array
                numb_row_dividers = row_id
                start_row_cell = ROW_OFFSET + row_id * 3 + numb_row_dividers
                numb_col_dividers = col_id + col_id // 3
                start_col_cell = COLUMN_OFFSET + col_id * 3 + numb_col_dividers
                view_array[
                    start_row_cell: start_row_cell + 3,
                    start_col_cell: start_col_cell + 3,
                ] = cell_view

        return view_array

    def __array_to_str(self, view_array: List[List[str]]) -> str:
        return "\n".join(["".join(row) for row in view_array])
