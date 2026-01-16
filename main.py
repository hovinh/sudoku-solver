from logzero import logger
from sudoku.utils import logging
from sudoku.problem import SudokuProblem
from sudoku.viewer import SudokuViewer

if __name__ == "__main__":
    logging.setup_logger()
    logger.info("Starting Sudoku Solver...")

    sudoku_problem = SudokuProblem(
        sudoku_string="000000010400000000020000000000050407008000300001090000300400200050100000000806000")
    viewer = SudokuViewer(sudoku_problem)
    viewer.log()
    logger.info("Sudoku Solver is running.")
