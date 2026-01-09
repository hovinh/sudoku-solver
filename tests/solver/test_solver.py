from sudoku.solver.solver import SudokuSolver
from sudoku.sudoku import SudokuPuzzle


def test_prune_solved_value_from_row_column_box():
    puzzle = SudokuPuzzle(
        sudoku_string='000000012003600000000007000410020000000500300700000600280000040000300500000000000')
    solver = SudokuSolver()

    prev_total_candidates = puzzle.count_total_candidates()
    solver.prune_solved_value_from_row_column_box(puzzle)
    new_total_candidates = puzzle.count_total_candidates()

    assert new_total_candidates < prev_total_candidates
