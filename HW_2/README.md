# Introduction to the OOP
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
## Task (Car racing):
You need to write a Car class that has the following attributes: fuel (initial fuel, set using random.randrange(0, 9)), trip_distance (distance travelled by the car), model (car model), and color. Implement a move method in the class that takes distance as an argument. The method should add the distance to trip_distance and reduce the fuel by the same amount.

Create 3 instances of this class.

In a loop while race_dist < desired_dist, for each car instance, call the move method and pass it a value from random.randrange(0, 9).

As soon as one of the cars has travelled a distance greater than or equal to desired_dist, display a message stating that the car has won, indicating its model and the distance travelled. The loop should then stop.

After the loop, display the distance travelled and remaining fuel for each car.
### Test execution
```bash
# ----------------unittest ----------------
python -m unittest HW_2.tests.test_unittest
# ---------------- pytest ----------------
pytest HW_2/tests/test_pytest.py -v  
```