from sudoku.sudoku import SudokuPuzzle


class SudokuSolver:
    def __init__(self):
        pass

    def solve(self, sudoku: SudokuPuzzle) -> None:
        """
        Solves the given Sudoku puzzle in place.

        Parameters
        ----------
        sudoku : SudokuPuzzle
            The Sudoku puzzle to be solved.
        """
        # Placeholder for the solving algorithm
        pass

    def prune_solved_value_from_row_column_box(self, sudoku: SudokuPuzzle) -> None:
        """
        Prunes solved values from the candidates of cells in the same row, column, and box.

        Parameters
        ----------
        sudoku : SudokuPuzzle
            The Sudoku puzzle whose candidates are to be pruned.
        """
        for cell in sudoku.iterate_over_cells():
            if cell.is_solved():
                solved_value = cell.value
                row_id = cell.row_id
                col_id = cell.col_id
                box_id = sudoku.to_box_id(row_id, col_id)

                # Prune from row
                row = sudoku.rows[row_id]
                for peer_cell in row:
                    if not peer_cell.is_solved() and (solved_value in peer_cell.candidates):
                        peer_cell.remove_candidate(solved_value)

                # Prune from column
                column = sudoku.columns[col_id]
                for peer_cell in column:

                    if not peer_cell.is_solved() and (solved_value in peer_cell.candidates):
                        peer_cell.remove_candidate(solved_value)

                # Prune from box
                box = sudoku.boxes[box_id]
                for peer_cell in box:
                    if not peer_cell.is_solved() and (solved_value in peer_cell.candidates):
                        peer_cell.remove_candidate(solved_value)
