from typing import Any, List, Tuple

from sudoku.unit.cell import SudokuCell


class SudokuCellGroup(object):
    """An interface for a group of SudokuCell objects."""

    def __init__(self, cells: List[Any]) -> None:
        """
        Initializes SudokuCellGroup instance.

        Parameters
        ----------
        cells : List[Any]
            A list of SudokuCell objects
        """
        self._cells = cells

    def __getitem__(self, index: int) -> SudokuCell:
        return self._cells[index]

    def __iter__(self):
        return iter(self._cells)

    def get_unique_candidates_and_belonging_cells(self) -> List[Tuple[int, SudokuCell]]:
        """
        Finds candidates that appear only once in the group and their corresponding cells.

        Returns
        -------
        List[Tuple[int, SudokuCell]]
            A list of tuples containing the unique candidate value and its corresponding SudokuCell.
        """
        candidate_count = dict()
        candidate_cell_map = dict()

        for cell in self._cells:
            for candidate in cell.candidates:
                if candidate in candidate_count:
                    candidate_count[candidate] += 1
                else:
                    candidate_count[candidate] = 1
                    candidate_cell_map[candidate] = cell

        unique_candidates = [
            (candidate, candidate_cell_map[candidate])
            for candidate, count in candidate_count.items()
            if count == 1  # occur only once
        ]

        return unique_candidates


class SudokuRow(SudokuCellGroup):
    """A class representing a row of cells in a Sudoku puzzle."""

    def __init__(self, cells: List[SudokuCell]) -> None:
        """
        Initializes SudokuRow instance.

        Parameters
        ----------
        cells : List[SudokuCell]
            A list of SudokuCell objects
        """
        super().__init__(cells)


class SudokuColumn(SudokuCellGroup):
    """A class representing a column of cells in a Sudoku puzzle."""

    def __init__(self, cells: List[SudokuCell]) -> None:
        """
        Initializes SudokuColumn instance.

        Parameters
        ----------
        cells : List[SudokuCell]
            A list of SudokuCell objects
        """
        super().__init__(cells)


class SudokuBox(SudokuCellGroup):
    """A class representing a box of cells in a Sudoku puzzle."""

    def __init__(self, cells: List[SudokuCell]) -> None:
        """
        Initializes SudokuBox instance.

        Parameters
        ----------
        cells : List[SudokuCell]
            A list of SudokuCell objects
        """
        super().__init__(cells)
