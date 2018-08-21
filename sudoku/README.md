# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: *Student should provide answer here*

The algorithm consists of (1) finding the twins, and (2) using knowledge of the twins to impose additional constraints on boxes in the same units as the twins. The constraints on the boxes in the same units as twins allows us to remove digits from their possible values

Extra care was made in the code to make sure various scenarios were avoided:
-Deletion of one of the twins (since it is also part of the same unit)
-Not to delete boxes with only one digit
-To incorporate diagonals as an extra one or two unit considerations, for some boxes (since not all boxes are part of diagonal units)
-To confine the search for matching digits to only the same unit as both twins are located
-To not treat the sequential two-digit pairing of the twins' digits as a whole, since they are not guaranteed to be paired the same way in other boxes (e.g. twins with value '17', with a box of value '1357' in the same unit, thus searching for '17' would lead to errors. Digit-wise search of matching digits from twins was used

The 'naked_twins' function is used as part of the 'reduce_puzzle' function, after 'eliminate' and 'only_choice' functions. When used in 'search' function, 'naked_twins' is propagated throughout the search tree implemented by the recursive search algorithm to help solve the Sudoku

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: *Student should provide answer here*

Diagonal Sudoku required extra checks to make sure certain boxes would be checked against an additional unit of boxes (or two units in the case of E5). This expanded the set of peers for some of the boxes and thus more boxes to check against the constraints in 'only_choice', 'eliminate', and 'naked_twins' functions used inside the recursive search tree function

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

