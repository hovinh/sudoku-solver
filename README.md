# sudoku-solver

## Environment Setup

```bash
python -m pip install virtualenv
python -m venv py3.10-sudoku
py3.10-sudoku\Scripts\activate

pip install pip-tools
pip-compile -v --rebuild -o requirements.txt
pip-sync requirements.txt

python -m ipykernel install --user --name=py3.10-sudoku-kernel
```

## Note
Target:
- solving algorithm
- benchmark
- redo the implementation
- write in best readable way

data:
sudoku17: https://web.archive.org/web/20131019184812if_/http://school.maths.uwa.edu.au/~gordon/sudokumin.php 


dataset:
https://github.com/t-dillon/tdoku/tree/master/benchmarks


Data
- grid 9x9
- candidate map? calculating blueprint, only confirm then update the grid
- represent candidate of grid 9x9x10 using boolean.
- number of candidate in cell
- sudoku line check: rows, columns.
- sudoku square check 3x3 box
- a way to map coordinate to which row, cell, or box
- box = row /3 *3 + col/3

Solving puzzle


Generate puzzle