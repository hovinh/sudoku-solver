from typing import List, Tuple

from sudoku import constant
from sudoku.sudoku import SudokuPuzzle
from sudoku.unit.cell import SudokuCell


class SolvingStrategy:
    """Base class for solving strategies."""

    def apply(self, sudoku):
        """
        Applies the solving strategy to the given Sudoku puzzle.

        Parameters
        ----------
        sudoku : SudokuPuzzle
            The Sudoku puzzle to which the strategy is applied.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    def __str__(self):
        return self.__class__.__name__


class UniqueStrategy(SolvingStrategy):
    """Implements the Unique solving strategy."""

    def apply(self, sudoku: SudokuPuzzle) -> SudokuPuzzle:
        """
        Applies the Unique strategy to the given Sudoku puzzle.
        Idea:
        Step 1
        - For each cell that is already solved, remove its value from the candidates
          of all other cells in the same row, column, and box.

        Step 2
        - For each unit (row, column, box), identify candidates that appear only once.
        - If a candidate is unique to a cell within that unit, set that cell's value
        to the candidate.

        Parameters
        ----------
        sudoku : SudokuPuzzle
            The Sudoku puzzle to which the strategy is applied.
        """
        # Initial cleanup: prune known solved values from peers
        for cell in sudoku.iterate_over_cells():
            self.prune_solved_value_from_units_containing_cell(sudoku, cell)

        # Find and fill hidden singles
        for unit in sudoku.iterate_over_all_units():
            unique_candidates: List[Tuple[int, SudokuCell]] = (
                unit.get_unique_candidates_and_belonging_cells()
            )
            for candidate, cell in unique_candidates:
                cell.remove_all_candidates_except(candidate)
                self.prune_solved_value_from_units_containing_cell(sudoku, cell)

        return sudoku

    def prune_solved_value_from_units_containing_cell(
        self, sudoku: SudokuPuzzle, cell: SudokuCell
    ) -> None:
        """
        Prunes solved values from the candidates of cells in the
        same row, column, and box.

        Parameters
        ----------
        sudoku : SudokuPuzzle
            The Sudoku puzzle to which the strategy is applied.
        cell : SudokuCell
            The Sudoku cell whose solved value is to be pruned from its peers.
        """

        def is_not_solved_and_contains_prunable_value(
            cell: SudokuCell, value: int
        ) -> bool:
            return (not cell.is_solved()) and (value in cell.candidates)

        if cell.is_solved():
            solved_value = cell.value
            row_id = cell.row_id
            col_id = cell.col_id
            box_id = sudoku.to_box_id(row_id, col_id)

            # Prune from row
            row = sudoku.rows[row_id]
            for peer_cell in row:
                if is_not_solved_and_contains_prunable_value(peer_cell, solved_value):
                    peer_cell.remove_candidate(solved_value)

            # Prune from column
            column = sudoku.columns[col_id]
            for peer_cell in column:
                if is_not_solved_and_contains_prunable_value(peer_cell, solved_value):
                    peer_cell.remove_candidate(solved_value)

            # Prune from box
            box = sudoku.boxes[box_id]
            for peer_cell in box:
                if is_not_solved_and_contains_prunable_value(peer_cell, solved_value):
                    peer_cell.remove_candidate(solved_value)


class HiddenCandidatePairStrategy(SolvingStrategy):
    """Implements the Hidden Candidate Pair solving strategy."""

    def apply(self, sudoku: SudokuPuzzle) -> SudokuPuzzle:
        """
        Applies the Hidden Candidate Pair strategy to the given Sudoku puzzle.
        Idea:
            - Identify pairs of candidates that appear together in exactly two
            cells within a unit (row, column, or box).
            - If such a pair is found, remove all other candidates from those two cells.

        Parameters
        ----------
        sudoku : SudokuPuzzle
            The Sudoku puzzle to which the strategy is applied.
        """
        # For each unit (row, column, box)
        for unit in sudoku.iterate_over_all_units():
            candidate_cell_map = dict()

            # Build a mapping of candidates to the cells they appear in
            for cell in unit:
                for candidate in cell.candidates:
                    if candidate not in candidate_cell_map:
                        candidate_cell_map[candidate] = []
                    candidate_cell_map[candidate].append(cell)

            # Identify potential hidden pairs
            potential_hidden_pairs = [
                (candidate, cells)
                for candidate, cells in candidate_cell_map.items()
                if len(cells) == 2  # appear in exactly two cells
            ]

            # Check for pairs of candidates that appear together in the same two cells
            for candidate, cells in potential_hidden_pairs:
                for other_candidate, other_cells in potential_hidden_pairs:
                    found_hidden_pair = (candidate != other_candidate) and (
                        cells == other_cells
                    )
                    if found_hidden_pair:
                        for cell in cells:
                            cell.set_candidates([candidate, other_candidate])

        return sudoku


class HiddenCandidateTripletStrategy(SolvingStrategy):
    """Implements the Hidden Candidate Triplet solving strategy."""

    def apply(self, sudoku: SudokuPuzzle) -> SudokuPuzzle:
        """
        Applies the Hidden Candidate Triplet strategy to the given Sudoku puzzle.
        Idea:
            - Identify triplets of candidates that appear together in exactly three
            cells within a unit (row, column, or box).
            - If such a triplet is found, remove all other candidates from
            those three cells.

        Parameters
        ----------
        sudoku : SudokuPuzzle
            The Sudoku puzzle to which the strategy is applied.
        """
        # For each unit (row, column, box)
        for unit in sudoku.iterate_over_all_units():
            candidate_cell_map = dict()

            # Build a mapping of candidates to the cells they appear in
            for cell in unit:
                for candidate in cell.candidates:
                    if candidate not in candidate_cell_map:
                        candidate_cell_map[candidate] = []
                    candidate_cell_map[candidate].append(cell)

            # Identify potential hidden triplets
            potential_hidden_triplets = [
                (candidate, cells)
                for candidate, cells in candidate_cell_map.items()
                if len(cells) == 3  # appear in exactly three cells
            ]

            # Check for triplets of candidates that appear together
            # in the same three cells
            for candidate, cells in potential_hidden_triplets:
                for other_candidate, other_cells in potential_hidden_triplets:
                    for another_candidate, another_cells in potential_hidden_triplets:
                        different_candidates = (
                            len(set([candidate, other_candidate, another_candidate]))
                            == 3
                        )
                        found_hidden_triplet = different_candidates and (
                            cells == other_cells == another_cells
                        )
                        if found_hidden_triplet:
                            for cell in cells:
                                cell.set_candidates(
                                    [candidate, other_candidate, another_candidate]
                                )

        return sudoku


class NakedPairStrategy(SolvingStrategy):
    """Implements the Naked Pair solving strategy."""

    def apply(self, sudoku: SudokuPuzzle) -> SudokuPuzzle:
        """
        Applies the Naked Pair strategy to the given Sudoku puzzle.
        Idea:
            - Identify pairs of cells within a unit (row, column, or box) that
            contain exactly the same two candidates.
            - If such a pair is found, remove those two candidates from all
            other cells in that unit.

        Parameters
        ----------
        sudoku : SudokuPuzzle
            The Sudoku puzzle to which the strategy is applied.
        """
        # For each unit (row, column, box)
        for unit in sudoku.iterate_over_all_units():
            # Find all cells with exactly two candidates
            two_candidate_cells = [cell for cell in unit if len(cell.candidates) == 2]

            # Check for naked pairs
            for i in range(len(two_candidate_cells)):
                for j in range(i + 1, len(two_candidate_cells)):
                    cell1 = two_candidate_cells[i]
                    cell2 = two_candidate_cells[j]
                    if cell1.candidates == cell2.candidates:
                        # Found a naked pair; remove these candidates
                        # from other cells in the unit
                        pair_candidates = cell1.candidates
                        for peer_cell in unit:
                            if peer_cell not in (cell1, cell2):
                                for candidate in pair_candidates:
                                    peer_cell.remove_candidate(candidate)

        return sudoku


class BoxLineInterpolationStrategy(SolvingStrategy):
    """Implements the Box-Line Interpolation solving strategy."""

    def apply(self, sudoku: SudokuPuzzle) -> SudokuPuzzle:
        """
        Applies the Box-Line Interpolation strategy to the given Sudoku puzzle.
        Idea:
            - For each box, check if a candidate is confined to a single row
            or column within that box.
            - If so, remove that candidate from the cells in the corresponding row
            or column outside of that box.

        Parameters
        ----------
        sudoku : SudokuPuzzle
            The Sudoku puzzle to which the strategy is applied.
        """
        for box in sudoku.iterate_over_boxes():
            candidate_positions = dict()

            # Map candidates to their positions within the box
            for cell in box:
                for candidate in cell.candidates:
                    if candidate not in candidate_positions:
                        candidate_positions[candidate] = []
                    candidate_positions[candidate].append(cell)

            # Check each candidate's positions
            for candidate, cells in candidate_positions.items():
                if len(cells) > 1:
                    rows = set(cell.row_id for cell in cells)
                    cols = set(cell.col_id for cell in cells)

                    # If confined to a single row, remove this candidate
                    # from that row's cells outside the box
                    if len(rows) == 1:
                        row_id = rows.pop()
                        for cell in sudoku.rows[row_id]:
                            if cell not in cells:
                                cell.remove_candidate(candidate)

                    # If confined to a single column, remove this candidate
                    # from that column's cells outside the box
                    if len(cols) == 1:
                        col_id = cols.pop()
                        for cell in sudoku.columns[col_id]:
                            if cell not in cells:
                                cell.remove_candidate(candidate)

        return sudoku


class BoxLineExtrapolationStrategy(SolvingStrategy):
    """Implements the Box-Line Extrapolation solving strategy."""

    def apply(self, sudoku: SudokuPuzzle) -> SudokuPuzzle:
        """
        Applies the Box-Line Extrapolation strategy to the given Sudoku puzzle.
        Idea:
            - For each row and column, check if a candidate is confined to a
            single box within that row or column.
            - If so, remove that candidate from other cells within that box.

        Parameters
        ----------
        sudoku : SudokuPuzzle
            The Sudoku puzzle to which the strategy is applied.
        """
        # Check rows
        for row in sudoku.iterate_over_rows():
            candidate_positions = dict()

            # Map candidates to their positions within the row
            for cell in row:
                for candidate in cell.candidates:
                    if candidate not in candidate_positions:
                        candidate_positions[candidate] = []
                    candidate_positions[candidate].append(cell)

            # Check each candidate's positions
            for candidate, cells in candidate_positions.items():
                boxes = set(
                    sudoku.to_box_id(cell.row_id, cell.col_id) for cell in cells
                )

                # If confined to a single box, remove this candidate
                # from other cells in that box
                if len(boxes) == 1:
                    box_id = boxes.pop()
                    box = sudoku.boxes[box_id]
                    for box_cell in box:
                        if box_cell not in cells:
                            box_cell.remove_candidate(candidate)

        # Check columns
        for column in sudoku.iterate_over_columns():
            candidate_positions = dict()

            # Map candidates to their positions within the column
            for cell in column:
                for candidate in cell.candidates:
                    if candidate not in candidate_positions:
                        candidate_positions[candidate] = []
                    candidate_positions[candidate].append(cell)

            # Check each candidate's positions
            for candidate, cells in candidate_positions.items():
                boxes = set(
                    sudoku.to_box_id(cell.row_id, cell.col_id) for cell in cells
                )

                # If confined to a single box, remove this candidate
                # from other cells in that box
                if len(boxes) == 1:
                    box_id = boxes.pop()
                    box = sudoku.boxes[box_id]
                    for box_cell in box:
                        if box_cell not in cells:
                            box_cell.remove_candidate(candidate)

        return sudoku


class RectangleCornerReductionsStrategy(SolvingStrategy):
    """Implements the Rectangle Corner Reduction solving strategy."""

    def apply(self, sudoku: SudokuPuzzle) -> SudokuPuzzle:
        """
        Applies the Rectangle Corner Reduction strategy to the given Sudoku puzzle.
        Idea:
            - Identify rectangles formed by four cells in two rows and two columns
            that share the same candidate.
            - If such a rectangle is found, eliminate that candidate from the other
            cells in that two rows and two columns.

        Parameters
        ----------
        sudoku : SudokuPuzzle
            The Sudoku puzzle to which the strategy is applied.
        """
        # For each pair of rows
        STARTING_ROW_INDEX = 1
        ENDING_ROW_INDEX = constant.NUMBER_OF_ROWS
        STARTING_COL_INDEX = 1
        ENDING_COL_INDEX = constant.NUMBER_OF_COLUMNS
        for top_left_corner in sudoku.iterate_over_cells():
            for bottom_right_corner in sudoku.iterate_over_cells():
                if (bottom_right_corner.row_id > top_left_corner.row_id) and (
                    bottom_right_corner.col_id > top_left_corner.col_id
                ):
                    top_right_corner = sudoku[
                        top_left_corner.row_id, bottom_right_corner.col_id
                    ]
                    bottom_left_corner = sudoku[
                        bottom_right_corner.row_id, top_left_corner.col_id
                    ]

                    # Find common candidates among the four corners
                    common_candidates = set(top_left_corner.candidates).intersection(
                        set(top_right_corner.candidates),
                        set(bottom_left_corner.candidates),
                        set(bottom_right_corner.candidates),
                    )

                    for candidate in common_candidates:
                        # Eliminate candidate from other cells
                        # in the two rows and two columns
                        for col_id in range(STARTING_COL_INDEX, ENDING_COL_INDEX + 1):
                            if col_id not in (
                                top_left_corner.col_id,
                                bottom_right_corner.col_id,
                            ):
                                sudoku[top_left_corner.row_id, col_id].remove_candidate(
                                    candidate
                                )
                                sudoku[
                                    bottom_right_corner.row_id, col_id
                                ].remove_candidate(candidate)

                        for row_id in range(STARTING_ROW_INDEX, ENDING_ROW_INDEX + 1):
                            if row_id not in (
                                top_left_corner.row_id,
                                bottom_right_corner.row_id,
                            ):
                                sudoku[row_id, top_left_corner.col_id].remove_candidate(
                                    candidate
                                )
                                sudoku[
                                    row_id, bottom_right_corner.col_id
                                ].remove_candidate(candidate)

        return sudoku
