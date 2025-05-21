class SudokuCell(object):
    def __init__(self):
        pass


class SudokuGrid(object):
    def __init__(self, sudoku_string: str):
        self.N_ROWS = 9
        self.N_COLS = 9
        self.sudoku_string = sudoku_string

    def __str__(self) -> str:
        def has_row_divider(row_id: int) -> bool:
            return (row_id % 3 == 0) and (row_id > 0)
        
        def has_col_divider(col_id: int) -> bool:
            return (col_id % 3 == 0) and (col_id > 0)
        text_str = ""
        row_divider = "- - - - - - - - - - -\n"
        last_col_id = 8
        for row_id in range(self.N_ROWS):
            if has_row_divider(row_id):
                text_str += row_divider

            for col_id in range(self.N_COLS):
                if has_col_divider(col_id):
                    text_str += '| '
                if col_id == last_col_id:
                    text_str += 


        return text_str


if __name__ == "__main__":
    grid = SudokuGrid(
        sudoku_string="000000010400000000020000000000050407008000300001090000300400200050100000000806000"
    )
    print(grid)
