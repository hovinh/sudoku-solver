from typing import List

from sudoku import constant


class SudokuCell(object):
    """Represents a cell in a Sudoku puzzle.

    Args:
        row_id (int): The row index of the cell on the Sudoku grid.
        col_id (int): The column index of the cell on the Sudoku grid.
        value (int, optional): The initial value of the cell.
            Defaults to constant.NO_SOLUTION_VALUE.
    """

    def __init__(
        self, row_id: int, col_id: int, value: int = constant.NO_SOLUTION_VALUE
    ) -> None:
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
            [self.value]
            if self.is_solved()
            else constant.DEFAULT_POSSIBLE_CELL_VALUE.copy()
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
        if new_value not in constant.DEFAULT_POSSIBLE_CELL_VALUE:
            raise ValueError(
                f"Value {new_value} is invalid. Must be in {constant.DEFAULT_POSSIBLE_CELL_VALUE}"
            )
        self._value = new_value

    """
    Candidates management.
    Caution: modifying candidates may change the cell's value.
    """

    @property
    def candidates(self):
        return self._candidates

    @property
    def number_of_candidates(self):
        return len(self._candidates)

    def remove_candidate(self, value: int) -> None:
        if value in self._candidates:
            self._candidates.remove(value)
        if self.number_of_candidates == 1:
            self._value = self._candidates[0]

    def remove_all_candidates_except(self, value: int) -> None:
        if value in self._candidates:
            self._candidates = [value]
            self._value = value

    def set_candidates(self, candidates: List[int]) -> None:
        self._candidates = candidates
        if self.number_of_candidates == 1:
            self._value = self._candidates[0]

    def is_solved(self):
        return self.value != constant.NO_SOLUTION_VALUE

    def __str__(self):
        return f"(value: {self._value}, row_id: {self._row_id}, col_id: {self._col_id})"
