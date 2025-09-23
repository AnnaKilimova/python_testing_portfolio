# Working with data types
## Installation
### 1. Cloning a repository:
```bash
git clone git clone git clone https://github.com/AnnaKilimova/python_testing_portfolio.git
cd python_testing_portfolio
```
### 2. Creating and activating of a virtual environment:
#### For MacOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate    
```  
### For Windows:
```bash
venv\Scripts\activate    
```
### 3. Installing dependencies:
```bash
pip install -r requirements.txt    
```
## Task 1 (Strings):
* Write a function that takes a string and returns its length.
* Create a function that takes two strings and returns a concatenated string.
### Test execution
```bash
# ----------------unittest ----------------
python -m unittest HW_1/task_1/unit_tests/test_single.py
python -m unittest HW_1/task_1/unit_tests/test_subtest.py
python -m unittest HW_1/task_1/unit_tests/test_parameterized.py
python -m HW_1.task_1.unit_tests.run_all_tests
# ---------------- pytest ----------------
pytest HW_1/task_1/py_tests/test_single.py -v
pytest HW_1/task_1/py_tests/test_parameterize.py -v
pytest HW_1/task_1/py_tests/test_fixture.py -v
pytest HW_1/task_1/py_tests/test_class.py -v   
```
## Task 2 (Int/Float):
* Implement a function that takes a number and returns its square.
* Create a function that takes two numbers and returns their sum.
* Create a function that takes two int numbers, performs a division operation, and returns the quotient and remainder.
### Test execution
```bash
# ----------------unittest ----------------
python -m unittest HW_1/task_2/tests/test_unittest.py
# ---------------- pytest ----------------
pytest HW_1/task_2/tests/test_pytest.py -v
```
## Task 3 (Lists):
* Write a function to calculate the average value of a list of numbers.
* Implement a function that takes two lists and returns a list containing the common elements of both lists.
### Test execution
```bash
# ----------------unittest ----------------
python -m unittest HW_1/task_3/tests/test_unittest.py
# ---------------- pytest ----------------
pytest HW_1/task_3/tests/test_pytest.py -v
```
## Task 4 (Dictionaries):
* Create a function that takes a dictionary and outputs all the keys in that dictionary.
* Implement a function that takes two dictionaries and returns a new dictionary that is a union of both dictionaries.
### Test execution
```bash
# ----------------unittest ----------------
python -m unittest HW_1/task_4/tests/test_unittest.py
# ---------------- pytest ----------------
pytest HW_1/task_4/tests/test_pytest.py -v
```
## Task 5 (Sets):
* Write a function that takes two sets and returns their union.
* Create a function that checks whether one set is a subset of another.
```bash
# ----------------unittest ----------------
python -m unittest HW_1/task_5/tests/test_unittest.py
# ---------------- pytest ----------------
python_testing_portfolio % pytest HW_1/task_5/tests/test_pytest.py -v
```
## Task 6 (Conditional expressions and loops):
* Implement a function that takes a number and outputs ‘Even’ if the number is even, and ‘Odd’ if it is odd.
* Create a function that takes a list of numbers and returns a new list containing only even numbers.
```bash
** Note: ** This last task does not include automated tests. Outputs are demonstrated using `print` statements within the code file.
```