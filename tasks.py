from invoke import task


@task
def lint(c):
    """Run code linters."""
    c.run("flake8 sudoku_solver tests")


@task
def test(c):
    """Run the test suite."""
    c.run("pytest")


@task
def format(c):
    """Format code using Black."""
    c.run("black sudoku_solver tests && isort sudoku_solver tests")


@task(pre=[format, lint, test])
def all(c):
    """Run all tasks: format, lint, and test."""
    print("All tasks completed successfully.")
