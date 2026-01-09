
from typing import Any, Tuple, List
from sudoku.unit.cell import SudokuCell


class SudokuCellGroup(object):
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

    def get_unique_candidate_in_sequence(self) -> List[Tuple[SudokuCell, int]]:
        """
        Finds candidates that appear only once in the group.

        Returns
        -------
        List[Tuple[SudokuCell, int]]
            A list of tuples containing the SudokuCell and its unique candidate value.
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
            (candidate_cell_map[candidate], candidate)
            for candidate, count in candidate_count.items()
            if count == 1  # occur only once
        ]

        return unique_candidates


class SudokuRow(SudokuCellGroup):
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
    def __init__(self, cells: List[SudokuCell]) -> None:
        """
        Initializes SudokuBox instance.

        Parameters
        ----------
        cells : List[SudokuCell]
            A list of SudokuCell objects
        """
        super().__init__(cells)
