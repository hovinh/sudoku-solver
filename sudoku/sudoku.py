from typing import Tuple

import numpy as np

from sudoku import constant
from sudoku.unit.cell import SudokuCell
from sudoku.unit.cell_group import SudokuBox, SudokuColumn, SudokuRow


class SudokuPuzzle(object):
    """A class representing a Sudoku puzzle."""

    def __init__(self, sudoku_string: str) -> None:
        """
        Initializes Sudoku instance.

        Parameters
        ----------
        sudoku_string : str
            A string of length 81 containing the Sudoku puzzle to be solved.
            The string should be a flat representation of the Sudoku grid,
            with each character representing the value of the cell in the
            order of row-major order.

        Attributes
        ----------
        grid : np.array
            A 2D array of SudokuCell objects representing the cells in the Sudoku grid.
            Valid indices are from (1,1) to (9,9).
        rows : np.array
            An array of SudokuRow objects representing the rows in the Sudoku grid.
            Valid indices are from 1 to 9.
        cols : np.array
            An array of SudokuColumn objects representing the columns in the Sudoku grid.
            Valid indices are from 1 to 9.
        boxes : np.array
            An array of SudokuBox objects representing the boxes in the Sudoku grid.
            Valid indices are from 1 to 9.

        Returns
        -------
        None
        """
        self.grid = self.__setup_grid(sudoku_string)
        self.rows = self.__setup_rows()
        self.columns = self.__setup_columns()
        self.boxes = self.__setup_boxes()

    def __setup_grid(self, sudoku_string: str):
        """
        Creates a 2D array of SudokuCell objects from a flat string representation
        of the Sudoku grid.

        Parameters
        ----------
        sudoku_string : str
            A string of length 81 containing the Sudoku puzzle to be solved.

        Returns
        -------
        np.array
            A 2D array of SudokuCell objects representing the cells in the Sudoku grid.
        """
        str_id = 0
        grid = list()
        STARTING_INDEX = 1
        ENDING_ROW_INDEX = constant.NUMBER_OF_ROWS
        ENDING_COLUMN_INDEX = constant.NUMBER_OF_COLUMNS

        # Offset index by 1 to make grid[1,1] the first cell
        grid.append([None] * (ENDING_COLUMN_INDEX + 1))

        # Create cells row by row
        for row_id in range(STARTING_INDEX, ENDING_ROW_INDEX + 1, 1):
            row = [None]  # Offset index by 1
            for col_id in range(STARTING_INDEX, ENDING_COLUMN_INDEX + 1, 1):
                cell_value = int(sudoku_string[str_id])
                cell = SudokuCell(row_id, col_id, cell_value)
                row.append(cell)
                str_id += 1
            grid.append(row)
        return np.array(grid)

    def __setup_rows(self) -> np.array:
        """
        Creates an array of SudokuRow objects from the Sudoku grid.

        Returns
        -------
        np.array
            An array of SudokuRow objects representing the rows in the Sudoku grid.
        """
        OFFSET_ROW = [None]
        STARTING_ROW_INDEX = 1
        STARTING_COLUMN_INDEX = 1
        ENDING_ROW_INDEX = constant.NUMBER_OF_ROWS
        rows = np.array(
            OFFSET_ROW
            + [
                SudokuRow(self.grid[row_id, STARTING_COLUMN_INDEX:])
                for row_id in range(STARTING_ROW_INDEX, ENDING_ROW_INDEX + 1, 1)
            ]
        )
        return rows

    def __setup_columns(self) -> np.array:
        """
        Creates an array of SudokuColumn objects from the Sudoku grid.

        Returns
        -------
        np.array
            An array of SudokuColumn objects representing the columns in the Sudoku grid.
        """
        OFFSET_COL = [None]
        STARTING_ROW_INDEX = 1
        STARTING_COL_INDEX = 1
        ENDING_COL_INDEX = constant.NUMBER_OF_COLUMNS
        cols = np.array(
            OFFSET_COL
            + [
                SudokuColumn(self.grid[STARTING_ROW_INDEX:, col_id])
                for col_id in range(STARTING_COL_INDEX, ENDING_COL_INDEX + 1, 1)
            ]
        )
        return cols

    def __setup_boxes(self) -> np.array:
        """
        Creates an array of SudokuBox objects from the Sudoku grid.

        Returns
        -------
        np.array
            An array of SudokuBox objects representing the boxes in the Sudoku grid.
        """
        OFFSET_BOX = [None]
        boxes = OFFSET_BOX.copy()
        BOX_WIDTH = constant.BOX_WIDTH
        STARTING_BOX_INDEX = 1
        ENDING_BOX_INDEX = constant.NUMBER_OF_BOXES
        for box_id in range(STARTING_BOX_INDEX, ENDING_BOX_INDEX + 1, 1):
            # Map box id to row and column indices
            start_row_id = ((box_id - 1) // BOX_WIDTH) * BOX_WIDTH + 1
            end_row_id = start_row_id + BOX_WIDTH
            start_col_id = ((box_id - 1) % BOX_WIDTH) * BOX_WIDTH + 1
            end_col_id = start_col_id + BOX_WIDTH

            # Extract cells in the box
            box = SudokuBox(
                self.grid[start_row_id:end_row_id, start_col_id:end_col_id].flatten()
            )
            boxes.append(box)
        return np.array(boxes)

    def __getitem__(self, index: Tuple[int, int]) -> SudokuCell:
        """
        Returns a SudokuCell object at the given index.

        Parameters
        ----------
        index : Tuple[int, int]
            A tuple of two integers, representing the row and column indices
            of the cell in the grid.

        Returns
        -------
        SudokuCell
            The SudokuCell object at the given index.

        Raises
        ------
        TypeError
            If the index is not a tuple of two integers.

        Examples
        --------
        >>> sudoku_problem = SudokuProblem(sudoku_string)
        >>> cell = sudoku_problem[1, 2]
        >>> cell
        SudokuCell(value=5, row_id=1, col_id=2)
        """
        if isinstance(index, tuple) and len(index) == 2:
            i, j = index
            if (1 <= i <= constant.NUMBER_OF_ROWS) and (
                1 <= j <= constant.NUMBER_OF_COLUMNS
            ):
                return self.grid[i, j]
            else:
                raise IndexError(
                    f"Index ({i}, {j}) is out of range. Valid indices are from"
                    f"(1,1) to ({constant.NUMBER_OF_ROWS},{constant.NUMBER_OF_COLUMNS})."
                )
        else:
            raise TypeError("Invalid index. Use obj[i, j] syntax.")

    def iterate_over_cells(self):
        """Public method to iterate over internal items."""
        flattened_grid = [c for c in self.grid.flatten() if c is not None]
        for cell in flattened_grid:
            yield cell

    def iterate_over_rows(self):
        """Public method to iterate over rows."""
        for row in self.rows[1:]:
            yield row

    def iterate_over_columns(self):
        """Public method to iterate over columns."""
        for column in self.columns[1:]:
            yield column

    def iterate_over_boxes(self):
        """Public method to iterate over boxes."""
        for box in self.boxes[1:]:
            yield box

    def iterate_over_all_units(self):
        """Public method to iterate over all units (rows, columns, boxes)."""
        for row in self.iterate_over_rows():
            yield row
        for column in self.iterate_over_columns():
            yield column
        for box in self.iterate_over_boxes():
            yield box

    def count_solved_cells(self) -> int:
        """
        Counts the number of solved cells in the Sudoku grid.

        Returns
        -------
        int
            The number of solved cells in the Sudoku grid.
        """
        # flatten grid to 1D array and skip None values
        return sum(1 for cell in self.iterate_over_cells() if cell.is_solved())

    def count_total_candidates(self) -> int:
        """
        Counts the total number of candidates across all cells in the Sudoku grid.

        Returns
        -------
        int
            The total number of candidates across all cells in the Sudoku grid.
        """
        return sum(cell.number_of_candidates for cell in self.iterate_over_cells())

    def is_solved(self) -> bool:
        """
        Checks if the Sudoku puzzle is completely solved.

        Returns
        -------
        bool
            True if all cells in the Sudoku grid are solved, False otherwise.
        """
        return self.count_solved_cells() == constant.NUMBER_OF_CELLS

    def to_box_id(self, row_id: int, col_id: int) -> int:
        """
        Converts row and column indices to box index.

        Parameters
        ----------
        row_id : int
            The row index of the cell in the grid.
        col_id : int
            The column index of the cell in the grid.

        Returns
        -------
        int
            The box index of the cell in the grid.
        """
        box_row = (row_id - 1) // constant.BOX_WIDTH
        box_col = (col_id - 1) // constant.BOX_WIDTH
        offset = 1  # To make box_id start from 1
        box_id = box_row * constant.BOX_WIDTH + box_col + offset

        # raise error if box_id is out of range
        if box_id < 1 or box_id > constant.NUMBER_OF_BOXES:
            raise ValueError(
                f"Box ID {box_id} is out of range. Must be between 1"
                f" and {constant.NUMBER_OF_BOXES}."
            )

        return box_id

    def __str__(self) -> str:
        """Returns a string representation of the Sudoku grid."""
        view_array = np.array(constant.DISPLAY_TEMPLATE)
        ROW_OFFSET = 2
        COLUMN_OFFSET = 6
        STARTING_ROW_INDEX = 1
        ENDING_ROW_INDEX = constant.NUMBER_OF_ROWS
        STARTING_COLUMN_INDEX = 1
        ENDING_COLUMN_INDEX = constant.NUMBER_OF_COLUMNS

        for row_id in range(STARTING_ROW_INDEX, ENDING_ROW_INDEX + 1, 1):
            for col_id in range(STARTING_COLUMN_INDEX, ENDING_COLUMN_INDEX + 1, 1):
                # Get the corresponding cell in the Sudoku problem and show
                # its value or candidates (if not solved)
                sudoku_cell = self[row_id, col_id]
                cell_view = constant.CELL_IS_NOT_FILLED_TEMPLATE.copy()
                if sudoku_cell.is_solved():
                    cell_view[1, :] = ["(", sudoku_cell.value, ")"]
                else:
                    # Extract candidates to show in the cell view
                    cell_view = np.array(
                        [
                            value if value in sudoku_cell.candidates else " "
                            for value in constant.DEFAULT_POSSIBLE_CELL_VALUE
                        ]
                    ).reshape(3, 3)

                # Calculate the starting position to place the cell view in the overall view array
                template_row_id = row_id - 1
                template_column_id = col_id - 1
                numb_row_dividers = template_row_id
                start_row_cell = ROW_OFFSET + template_row_id * 3 + numb_row_dividers
                numb_col_dividers = template_column_id + template_column_id // 3
                start_col_cell = (
                    COLUMN_OFFSET + template_column_id * 3 + numb_col_dividers
                )
                view_array[
                    start_row_cell : start_row_cell + 3,
                    start_col_cell : start_col_cell + 3,
                ] = cell_view

        return "\n".join(["".join(row) for row in view_array])
