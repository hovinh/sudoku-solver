from sudoku.sudoku import SudokuPuzzle


def test_SudokuPuzzle():
    puzzle = SudokuPuzzle(
        sudoku_string="000000012003600000000007000410020000000500300700000600280000040000300500000000000"  # noqa: E501
    )

    number_of_cells = len(list(puzzle.iterate_over_cells()))
    assert number_of_cells == 81

    number_of_rows = len(list(puzzle.iterate_over_rows()))
    assert number_of_rows == 9

    number_of_columns = len(list(puzzle.iterate_over_columns()))
    assert number_of_columns == 9

    number_of_solved_cells = puzzle.count_solved_cells()
    assert number_of_solved_cells == 17

    box_ids = [
        puzzle.to_box_id(row_id, col_id)
        for row_id in range(1, 10)
        for col_id in range(1, 10)
    ]
    assert box_ids == [
        1,
        1,
        1,
        2,
        2,
        2,
        3,
        3,
        3,
        1,
        1,
        1,
        2,
        2,
        2,
        3,
        3,
        3,
        1,
        1,
        1,
        2,
        2,
        2,
        3,
        3,
        3,
        4,
        4,
        4,
        5,
        5,
        5,
        6,
        6,
        6,
        4,
        4,
        4,
        5,
        5,
        5,
        6,
        6,
        6,
        4,
        4,
        4,
        5,
        5,
        5,
        6,
        6,
        6,
        7,
        7,
        7,
        8,
        8,
        8,
        9,
        9,
        9,
        7,
        7,
        7,
        8,
        8,
        8,
        9,
        9,
        9,
        7,
        7,
        7,
        8,
        8,
        8,
        9,
        9,
        9,
    ]
