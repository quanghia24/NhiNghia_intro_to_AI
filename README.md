step1: create virtual environment

python -m venv .env

step2: activate that vir-env

em vào folder .env -> script -> Activate.ps1

DFS của em gồm 2 file là main.py và solver.py nghe
main.py là phần game, solver.py sẽ áp dụng giải thuật backtracking để giải nó

Implementation Steps :
    1. Fill the pygame window with Sudoku Board i.e., Construct a 9×9 grid. 
    2. Fill the board with default numbers. 
    3. Assign a specific key for each operations and listen it. 
    4. Integrate the backtracking algorithm into it. 
    5. Use set of colors to visualize auto solving.

