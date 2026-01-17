# Sudoku Solver

This repository contains an implementation of a Sudoku solver using Object-Oriented Programming (OOP) principles. The goal is to create a solver that is not only efficient but also easy to understand and maintain. The solver is implemented in Python, taking advantage of its built-in support for OOP.

The Sudoku game is a popular puzzle game where the player is given a 9x9 grid with some numbers already filled in. The goal is to fill in the remaining numbers such that each row, column, and 3x3 sub-grid contains the numbers 1-9 without repeating any number. The solver in this repository uses candidate removal-oriented algorithms to solve the puzzle.

## Folder Structure

```
📁 sudoku_solver
├── 📁 .vscode/             # VSCode settings
├── 📁 .venv/               # Python virtual environment
├── 📁 dataset/             # Input data for experimentation
├── 📁 logs/                # Log files
├── 📁 notebooks/           # Jupyter notebooks
├── 📁 sudoku/              # Main code
├── 📁 tests/               # Unit tests
├── 📄 .flake8              # Flake8-specific linting
├── 📄 .gitignore           # Ignore files/directories for Git version control
├── 📄 pytest.ini           # Pytest configuration
├── 📄 README.md            # Main documentation
├── 📄 requirements.in      # Python package dependencies
├── 📄 requirements.txt     # Python package dependencies
└── 📄 tasks.py             # Invoke tasks (lint, format, test)
```
- The Sudoku solver implementation in Python.
- Jupyter notebooks for experimentation and debugging.
- Unit tests for the solver.
- A dataset of Sudoku puzzles for testing and experimentation.

## Prerequisites

Before you start working with this project, make sure you have the followings:
- Python 3.11+ installed and available in your PATH.
- Virtual environment setup for dependency isolation:

```bash
# Create a virtual environment called '.venv'
py -m pip install virtualenv
py -m virtualenv .venv
.venv\Scripts\activate

# Install required packages
py -m pip install pip-tools
pip-compile -v --rebuild -o requirements.txt
pip-sync requirements.txt

# Add Jupyter kernel
py -m ipykernel install --user --name=sudoku-kernel
```

## References

Used dataset:  [sudoku17](https://web.archive.org/web/20131019184812if_/http://school.maths.uwa.edu.au/~gordon/sudokumin.php). 

## Notebooks

| Notebook (.ipynb) | Description | 
| - | - |
| experiments.ipynb| Experimenting best strategy combination.|
| troubleshoot.ipynb| Show how to troubleshoot solving strategies.|

## Contribution

- Contact point: Xuan Vinh (hovinh39@gmail.com).
- The repository is organized to make it easy to follow and contribute to. It is hoped that this implementation will be useful for those learning OOP principles and for those who want to implement their own Sudoku solver.

### PR Guideline
- The latest runnable branch is `master`.
- All new development should be done on a `feature` branch off `dev`.
    - Submit a Pull Request (PR) from your `feature` branch to `dev` for review and approval.
- **Before commiting changes**, ensure code quality by running:

```bash
invoke all
``` 
This command runs linting, formatting, and tests to maintain consistency and prevent issues.