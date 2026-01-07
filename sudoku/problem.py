from typing import List, Tuple, Any
import numpy as np
from sudoku.utils import constant


def has_row_divider(row_id: int) -> bool:
    return (row_id % constant.BOX_WIDTH == 0) and (row_id > 0)


def has_col_divider(col_id: int) -> bool:
    return (col_id % constant.BOX_WIDTH == 0) and (col_id > 0)


class SudokuCell(object):
    def __init__(self, row_id: int, col_id: int, value: int = constant.UNFILLED_VALUE) -> None:
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
            [self.value] if self.is_solved(
            ) else constant.DEFAULT_POSSIBLE_CELL_VALUE.copy()
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

    @property
    def candidates(self):
        return self._candidates

    @property
    def number_of_candidates(self):
        return len(self._candidates)

    def is_solved(self):
        return self.value != constant.UNFILLED_VALUE

    @property
    def solution(self):
        return None if self.number_of_candidates > 1 else self.candidates[0]

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

    def __iter__(self):
        # delegate iteration to the internal list
        return iter(self._cells)

    def get_unique_candidate_in_sequence(self) -> List[Tuple[SudokuCell, int]]:
        """
        Finds candidates that appear only once in the sequence.

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
            if count == 1
        ]

        return unique_candidates


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

    def __iter__(self):
        # delegate iteration to the internal 2D array flattened
        return iter(self._cells.flatten())

    def __str__(self):
        text_str = ""
        for row_id in range(constant.BOX_WIDTH):
            row_cells = self._cells[row_id, :]
            text_str += " ".join([f"{cell}" for cell in row_cells]) + "\n"
        return text_str

    def get_unique_candidate_in_sequence(self) -> List[Tuple[SudokuCell, int]]:
        """
        Finds candidates that appear only once in the box.

        Returns
        -------
        List[Tuple[SudokuCell, int]]
            A list of tuples containing the SudokuCell and its unique candidate value.
        """
        candidate_count = dict()
        candidate_cell_map = dict()

        for i in range(constant.BOX_WIDTH):
            for j in range(constant.BOX_WIDTH):
                cell = self._cells[i, j]
                for candidate in cell.candidates:
                    if candidate in candidate_count:
                        candidate_count[candidate] += 1
                    else:
                        candidate_count[candidate] = 1
                        candidate_cell_map[candidate] = cell

        unique_candidates = [
            (candidate_cell_map[candidate], candidate)
            for candidate, count in candidate_count.items()
            if count == 1
        ]

        return unique_candidates


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
        """
        Creates a 2D array of SudokuCell objects from a flat string representation of the Sudoku grid.

        Parameters
        ----------
        sudoku_string : str
            A string of length 81 containing the Sudoku puzzle to be solved.
            The string should be a flat representation of the Sudoku grid,
            with each character representing the value of the cell in the
            order of row-major order.

        Returns
        -------
        np.array
            A 2D array of SudokuCell objects representing the cells in the Sudoku grid.
        """
        str_id = 0
        grid = list()
        # Create cells row by row
        for row_id in range(1, constant.NUMB_ROWS+1, 1):
            row = list()
            for col_id in range(1, constant.NUMB_COLUMNS+1, 1):
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
        rows = np.array(
            OFFSET_ROW +
            [SudokuRow(self.grid[row_id, :])
             for row_id in range(constant.NUMB_ROWS)]
        )
        return rows

    def __setup_cols(self) -> np.array:
        """
        Creates an array of SudokuColumn objects from the Sudoku grid.

        Returns
        -------
        np.array
            An array of SudokuColumn objects representing the columns in the Sudoku grid.
        """
        OFFSET_COL = [None]
        cols = np.array(
            OFFSET_COL +
            [SudokuColumn(self.grid[:, col_id])
                for col_id in range(constant.NUMB_COLUMNS)
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
        boxes = list([None])  # Offset index by 1
        for box_id in range(constant.NUMB_BOXES):
            start_row_id = (box_id // constant.BOX_WIDTH) * constant.BOX_WIDTH
            end_row_id = start_row_id + 3
            start_col_id = (box_id % constant.BOX_WIDTH) * constant.BOX_WIDTH
            end_col_id = start_col_id + 3
            box = SudokuBox(
                self.grid[start_row_id:end_row_id, start_col_id:end_col_id])
            boxes.append(box)
        return boxes

    def __str__(self) -> str:
        text_str = ""
        last_col_id = 8
        for row_id in range(constant.NUMB_ROWS):
            if has_row_divider(row_id):
                text_str += constant.ROW_DIVIDER

            for col_id in range(constant.NUMB_COLUMNS):
                if has_col_divider(col_id):
                    text_str += "| "
                cell = self.grid[row_id, col_id]
                if col_id == last_col_id:
                    text_str += f"{cell.value} \n"
                else:
                    text_str += f"{cell.value} "

        return text_str

    def __getitem__(self, index: Tuple[int, int]) -> SudokuCell:
        """
        Returns a SudokuCell object at the given index.

        Parameters
        ----------
        index : Tuple[int, int]
            A tuple of two integers, representing the row and column indices of the cell in the grid.

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
        >>> cell = sudoku_problem[0, 0]
        >>> cell
        SudokuCell(value=5, row_id=0, col_id=0)
        """
        if isinstance(index, tuple) and len(index) == 2:
            i, j = index
            return self.grid[i, j]
        else:
            raise TypeError("Invalid index. Use obj[i, j] syntax.")

    def count_solved_cells(self) -> int:
        """
        Counts the number of solved cells in the Sudoku grid.

        Returns
        -------
        int
            The number of solved cells in the Sudoku grid.
        """
        count = 0
        for row in self.grid:
            for cell in row:
                if cell.is_solved():
                    count += 1
        return count

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
        if box_id < 1 or box_id > constant.NUMB_BOXES:
            raise ValueError(
                f"Box ID {box_id} is out of range. Must be between 1 and {constant.NUMB_BOXES}."
            )

        return box_id

    def prune_candidates_comprehensively(self) -> None:
        """
        Prunes the candidates for each cell in the Sudoku box/column/row that contained the solved cell.

        Returns
        -------
        None
        """

        for row in self.grid:
            for cell in row:
                self.prune_candidates_from_row_column_box(cell)

    def prune_candidates_from_row_column_box(self, cell: SudokuCell) -> None:
        """
        Prunes the candidates for each cell in the Sudoku box/column/row that contained the given cell.

        Parameters
        ----------
        cell : SudokuCell
            The SudokuCell object whose value will be used to prune candidates from its peers.

        Returns
        -------
        None
        """
        def is_not_solved_and_contains_prunable_value(cell: SudokuCell, value: int) -> bool:
            return (not cell.is_solved()) and (value in cell.candidates)

        if not cell.is_solved():
            return

        solved_value = cell.value
        row_id = cell.row_id
        col_id = cell.col_id

        # Prune candidates in the same row
        for peer_cell in self.rows[row_id]:
            if is_not_solved_and_contains_prunable_value(peer_cell, solved_value):
                peer_cell.remove_candidate(solved_value)

        # Prune candidates in the same column
        for peer_cell in self.cols[col_id]:
            if is_not_solved_and_contains_prunable_value(peer_cell, solved_value):
                peer_cell.remove_candidate(solved_value)

        # Prune candidates in the same box
        box_id = self.to_box_id(row_id, col_id)
        for peer_cell in self.boxes[box_id]:
            # for i in range(constant.BOX_WIDTH):
            #     for j in range(constant.BOX_WIDTH):
            #         peer_cell = self.boxes[box_id][i, j]
            if is_not_solved_and_contains_prunable_value(peer_cell, solved_value):
                peer_cell.remove_candidate(solved_value)

    def count_all_candidates(self) -> int:
        """
        Counts the total number of candidates across all cells in the Sudoku grid.

        Returns
        -------
        int
            The total number of candidates across all cells in the Sudoku grid.
        """
        total_candidates = 0
        for row in self.grid:
            for cell in row:
                total_candidates += cell.number_of_candidates
        return total_candidates

    def apply_hidden_single_strategy(self) -> None:
        """
        Applies the hidden single strategy to the Sudoku grid.

        Returns
        -------
        None
        """
        # Check rows for hidden singles
        for row in self.rows[1:]:
            unique_candidates: List[Tuple[SudokuCell, int]
                                    ] = row.get_unique_candidate_in_sequence()
            for cell, candidate in unique_candidates:
                cell.remove_all_candidates_except(candidate)
                self.prune_candidates_from_row_column_box(cell)

        # Check columns for hidden singles
        for col in self.cols[1:]:
            unique_candidates: List[Tuple[SudokuCell, int]
                                    ] = col.get_unique_candidate_in_sequence()
            for cell, candidate in unique_candidates:
                cell.remove_all_candidates_except(candidate)
                self.prune_candidates_from_row_column_box(cell)

        # Check boxes for hidden singles
        for box in self.boxes[1:]:
            unique_candidates: List[Tuple[SudokuCell, int]
                                    ] = box.get_unique_candidate_in_sequence()
            for cell, candidate in unique_candidates:
                cell.remove_all_candidates_except(candidate)
                self.prune_candidates_from_row_column_box(cell)

    def apply_hidden_pair_strategy(self) -> None:
        """
        Applies the hidden pair strategy to the Sudoku grid.

        Returns
        -------
        None
        """
        # Check rows for hidden pairs
        for row in self.rows[1:]:
            candidate_count = dict()
            candidate_cell_map = dict()

            for cell in row:
                for candidate in cell.candidates:
                    if candidate in candidate_count:
                        candidate_count[candidate] += 1
                        candidate_cell_map[candidate].append(cell)
                    else:
                        candidate_count[candidate] = 1
                        candidate_cell_map[candidate] = [cell]

            # Find hidden pairs
            hidden_pairs = [
                (candidate, cells)
                for candidate, cells in candidate_cell_map.items()
                if candidate_count[candidate] == 2
            ]

            # Eliminate other candidates from the cells in the hidden pair
            for candidate, cells in hidden_pairs:
                # Find the counterpart candidate in the hidden pair
                for other_candidate, other_cells in hidden_pairs:
                    if other_candidate != candidate and cells == other_cells:
                        for cell in cells:
                            cell.set_candidates([candidate, other_candidate])

        # Check columns for hidden pairs
        for col in self.cols[1:]:
            candidate_count = dict()
            candidate_cell_map = dict()

            for cell in col:
                for candidate in cell.candidates:
                    if candidate in candidate_count:
                        candidate_count[candidate] += 1
                        candidate_cell_map[candidate].append(cell)
                    else:
                        candidate_count[candidate] = 1
                        candidate_cell_map[candidate] = [cell]

            # Find hidden pairs
            hidden_pairs = [
                (candidate, cells)
                for candidate, cells in candidate_cell_map.items()
                if candidate_count[candidate] == 2
            ]

            # Eliminate other candidates from the cells in the hidden pair
            for candidate, cells in hidden_pairs:
                # Find the counterpart candidate in the hidden pair
                for other_candidate, other_cells in hidden_pairs:
                    if other_candidate != candidate and cells == other_cells:
                        for cell in cells:
                            cell.set_candidates([candidate, other_candidate])

        # Check boxes for hidden pairs
        for box in self.boxes[1:]:
            candidate_count = dict()
            candidate_cell_map = dict()

            for i in range(constant.BOX_WIDTH):
                for j in range(constant.BOX_WIDTH):
                    cell = box[i, j]
                    for candidate in cell.candidates:
                        if candidate in candidate_count:
                            candidate_count[candidate] += 1
                            candidate_cell_map[candidate].append(cell)
                        else:
                            candidate_count[candidate] = 1
                            candidate_cell_map[candidate] = [cell]

            # Find hidden pairs
            hidden_pairs = [
                (candidate, cells)
                for candidate, cells in candidate_cell_map.items()
                if candidate_count[candidate] == 2
            ]

            # Eliminate other candidates from the cells in the hidden pair
            for candidate, cells in hidden_pairs:
                # Find the counterpart candidate in the hidden pair
                for other_candidate, other_cells in hidden_pairs:
                    if other_candidate != candidate and cells == other_cells:
                        for cell in cells:
                            cell.set_candidates([candidate, other_candidate])

    def apply_hidden_group_strategy(self, group_size: int = 2) -> None:
        """
        Applies the hidden group strategy to the Sudoku grid.

        Parameters
        ----------
        group_size : int, default=2
            The size of the group to look for.

        Returns
        -------
        None
        """
        # Check rows for hidden groups
        for row in self.rows[1:]:
            candidate_count = dict()
            candidate_cell_map = dict()

            for cell in row:
                for candidate in cell.candidates:
                    if candidate in candidate_count:
                        candidate_count[candidate] += 1
                        candidate_cell_map[candidate].append(cell)
                    else:
                        candidate_count[candidate] = 1
                        candidate_cell_map[candidate] = [cell]

            # Find hidden groups
            hidden_groups = [
                (candidate, cells)
                for candidate, cells in candidate_cell_map.items()
                if candidate_count[candidate] == group_size
            ]

            # Among hidden groups, find sets of candidates that share the same cells
            seen_groups = dict()
            for candidate, cells in hidden_groups:
                cells_tuple = tuple(
                    sorted(cells, key=lambda c: (c.row_id, c.col_id)))
                if cells_tuple in seen_groups:
                    seen_groups[cells_tuple].append(candidate)
                else:
                    seen_groups[cells_tuple] = [candidate]

            # for k, v in seen_groups.items():
            #     print(
            #         f'k: {[[cell.row_id, cell.col_id, cell.candidates] for cell in k]}, v: {v}')

            # Eliminate other candidates from the cells in the hidden group
            for cells, candidates in seen_groups.items():
                if len(candidates) == group_size:  # Found a hidden group
                    # print(
                    #     f"Hidden group found in row: {[cell.candidates for cell in cells]}, candidates: {candidates}")

                    for cell in cells:
                        if cell.number_of_candidates > group_size:
                            print("Done")
                            cell.set_candidates(candidates)

        # Check columns for hidden groups
        for col in self.cols[1:]:
            candidate_count = dict()
            candidate_cell_map = dict()

            for cell in col:
                for candidate in cell.candidates:
                    if candidate in candidate_count:
                        candidate_count[candidate] += 1
                        candidate_cell_map[candidate].append(cell)
                    else:
                        candidate_count[candidate] = 1
                        candidate_cell_map[candidate] = [cell]

            # Find hidden groups
            hidden_groups = [
                (candidate, cells)
                for candidate, cells in candidate_cell_map.items()
                if candidate_count[candidate] == group_size
            ]

            # Among hidden groups, find sets of candidates that share the same cells
            seen_groups = dict()
            for candidate, cells in hidden_groups:
                cells_tuple = tuple(
                    sorted(cells, key=lambda c: (c.row_id, c.col_id)))
                if cells_tuple in seen_groups:
                    seen_groups[cells_tuple].append(candidate)
                else:
                    seen_groups[cells_tuple] = [candidate]

            # Eliminate other candidates from the cells in the hidden group
            for cells, candidates in seen_groups.items():
                if len(candidates) == group_size:  # Found a hidden group
                    for cell in cells:
                        if cell.number_of_candidates > group_size:
                            cell.set_candidates(candidates)

        # Check boxes for hidden groups
        for box in self.boxes[1:]:
            candidate_count = dict()
            candidate_cell_map = dict()

            for i in range(constant.BOX_WIDTH):
                for j in range(constant.BOX_WIDTH):
                    cell = box[i, j]
                    for candidate in cell.candidates:
                        if candidate in candidate_count:
                            candidate_count[candidate] += 1
                            candidate_cell_map[candidate].append(cell)
                        else:
                            candidate_count[candidate] = 1
                            candidate_cell_map[candidate] = [cell]

            # Find hidden groups
            hidden_groups = [
                (candidate, cells)
                for candidate, cells in candidate_cell_map.items()
                if candidate_count[candidate] == group_size
            ]

            # Among hidden groups, find sets of candidates that share the same cells
            seen_groups = dict()
            for candidate, cells in hidden_groups:
                cells_tuple = tuple(
                    sorted(cells, key=lambda c: (c.row_id, c.col_id)))
                if cells_tuple in seen_groups:
                    seen_groups[cells_tuple].append(candidate)
                else:
                    seen_groups[cells_tuple] = [candidate]

            # Eliminate other candidates from the cells in the hidden group
            for cells, candidates in seen_groups.items():
                if len(candidates) == group_size:  # Found a hidden group
                    for cell in cells:
                        if cell.number_of_candidates > group_size:
                            cell.set_candidates(candidates)

    def apply_naked_group_strategy(self, group_size: int = 2) -> None:
        """
        Applies the naked group strategy to the Sudoku grid.

        Parameters
        ----------
        group_size : int, default=2
            The size of the group to look for.

        Returns
        -------
        None
        """
        # Check rows for naked groups
        for row in self.rows[1:]:
            # Find all cells with exactly group_size candidates
            group_size_candidate_cells = [
                cell for cell in row if cell.number_of_candidates == group_size]
            # Find naked groups
            seen_groups = dict()
            for cell in group_size_candidate_cells:
                candidates_tuple = tuple(sorted(cell.candidates))
                if candidates_tuple in seen_groups:
                    seen_groups[candidates_tuple].append(cell)
                else:
                    seen_groups[candidates_tuple] = [cell]
            # Eliminate candidates from other cells
            for candidates, cells in seen_groups.items():
                if len(cells) == group_size:  # Found a naked group
                    for peer_cell in row:
                        if peer_cell not in cells and not peer_cell.is_solved():
                            for candidate in candidates:
                                peer_cell.remove_candidate(candidate)

        # Check columns for naked groups
        for col in self.cols[1:]:
            # Find all cells with exactly group_size candidates
            group_size_candidate_cells = [
                cell for cell in col if cell.number_of_candidates == group_size]
            # Find naked groups
            seen_groups = dict()
            for cell in group_size_candidate_cells:
                candidates_tuple = tuple(sorted(cell.candidates))
                if candidates_tuple in seen_groups:
                    seen_groups[candidates_tuple].append(cell)
                else:
                    seen_groups[candidates_tuple] = [cell]
            # Eliminate candidates from other cells
            for candidates, cells in seen_groups.items():
                if len(cells) == group_size:  # Found a naked group
                    for peer_cell in col:
                        if peer_cell not in cells and not peer_cell.is_solved():
                            for candidate in candidates:
                                peer_cell.remove_candidate(candidate)

        # Check boxes for naked groups
        for box in self.boxes[1:]:
            # Find all cells with exactly group_size candidates
            group_size_candidate_cells = [
                box[i, j]
                for i in range(constant.BOX_WIDTH)
                for j in range(constant.BOX_WIDTH)
                if box[i, j].number_of_candidates == group_size
            ]
            # Find naked groups
            seen_groups = dict()
            for cell in group_size_candidate_cells:
                candidates_tuple = tuple(sorted(cell.candidates))
                if candidates_tuple in seen_groups:
                    seen_groups[candidates_tuple].append(cell)
                else:
                    seen_groups[candidates_tuple] = [cell]

            # Eliminate candidates from other cells
            for candidates, cells in seen_groups.items():
                if len(cells) == group_size:  # Found a naked group
                    for i in range(constant.BOX_WIDTH):
                        for j in range(constant.BOX_WIDTH):
                            peer_cell = box[i, j]
                            if peer_cell not in cells and not peer_cell.is_solved():
                                for candidate in candidates:
                                    peer_cell.remove_candidate(candidate)

    def is_solved(self) -> bool:
        """
        Checks if the Sudoku puzzle is completely solved.

        Returns
        -------
        bool
            True if the Sudoku puzzle is completely solved, False otherwise.
        """
        return self.count_solved_cells() == constant.NUMBER_OF_CELLS
