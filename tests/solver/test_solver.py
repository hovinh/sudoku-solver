from sudoku.solver import Strategy, SudokuSolver
from sudoku.sudoku import SudokuPuzzle


def test_solve():
    puzzle = SudokuPuzzle(
        sudoku_string="000000012003600000000007000410020000000500300700000600280000040000300500000000000"  # noqa: E501
    )
    solver = SudokuSolver(strategies=[Strategy.UniqueStrategy()])

    prev_total_candidates = puzzle.count_total_candidates()
    puzzle = solver.solve(puzzle)
    new_total_candidates = puzzle.count_total_candidates()

    assert new_total_candidates < prev_total_candidates
