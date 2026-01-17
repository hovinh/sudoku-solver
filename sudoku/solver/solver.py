from typing import List

from logzero import logger

from sudoku.solver.strategy import SolvingStrategy
from sudoku.sudoku import SudokuPuzzle


class SudokuSolver:
    """Solves Sudoku puzzles using a sequence of solving strategies."""

    def __init__(self, strategies: List[SolvingStrategy] = []) -> None:
        self.strategies: List[SolvingStrategy] = strategies

    def solve(self, puzzle: SudokuPuzzle, verbose: bool = False) -> SudokuPuzzle:
        """
        Solves the given Sudoku puzzle in place.

        Parameters
        ----------
        sudoku : SudokuPuzzle
            The Sudoku puzzle to be solved.
        verbose : bool, optional
            If True, prints progress information during solving. Default is False.
        """
        if len(self.strategies) == 0:
            raise ValueError("No solving strategies provided.")

        last_total_number_of_candidates = puzzle.count_total_candidates()
        if verbose:
            logger.info(f"Initial total candidates: {last_total_number_of_candidates}")
            logger.info(f"\n{puzzle}")
        while True:
            # Try each strategy in sequence and
            strategy_index = 0
            current_total_number_of_candidates = last_total_number_of_candidates

            while strategy_index < len(self.strategies):
                strategy = self.strategies[strategy_index]
                puzzle = strategy.apply(puzzle)
                current_total_number_of_candidates = puzzle.count_total_candidates()
                made_progress = (
                    current_total_number_of_candidates < last_total_number_of_candidates
                )
                if made_progress:
                    if verbose:
                        logger.info(
                            f"Strategy {strategy.__class__.__name__} applied,"
                            f"reduced candidates from {last_total_number_of_candidates}"
                            f" to {current_total_number_of_candidates}"
                        )
                        logger.info(f"\n{puzzle}")
                    break
                else:
                    strategy_index += 1  # Move to the next strategy

            has_solved = puzzle.is_solved()
            if has_solved:
                if verbose:
                    logger.info("Puzzle solved!")
                break

            no_new_progress = (
                current_total_number_of_candidates == last_total_number_of_candidates
            )
            if no_new_progress:
                break

            last_total_number_of_candidates = current_total_number_of_candidates
        return puzzle
