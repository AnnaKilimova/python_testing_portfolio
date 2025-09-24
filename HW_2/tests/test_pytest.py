import pytest
from unittest.mock import patch
from ..main import Car

def test_init_fuel_trip_distance_model_color():
    """   
    Test the correct initialization of a Car object.

    Verifies that upon creation:
      - the model is set correctly,
      - the color is set correctly,
      - fuel is correctly assigned via patch,
      - trip_distance is initialized to zero.

    Uses:
        patch to fix the random fuel value for deterministic testing.

    Assertions:
        assert c.model == expected model
        assert c.color == expected color
        assert c.fuel == mocked fuel value
        assert c.trip_distance == 0
    """
    with patch("HW_2.main.random.randrange", return_value=5):
        c = Car("BMW_X6", "white")
    assert c.model == "BMW_X6"
    assert c.color == "white"
    assert c.fuel == 5
    assert c.trip_distance == 0

@pytest.mark.parametrize("input_fuel,input_distance,expected_trip_distance,expected_fuel", [
    (5, 3, 3, 2),  # normal case
    (5, 5, 5, 0),  # enough fuel
    (5, 7, 5, 0),  # attempt to drive more than there is
    (0, 4, 0, 0),  # no fuel
    (4, 0, 0, 4),  # moving at 0
])
def test_move_behaviour(input_fuel: int, input_distance: int, expected_trip_distance: int, expected_fuel: int) -> None:
    """
    Test the move() method of the Car class.

    Args (parameters via pytest parametrize):
        input_fuel (int): starting fuel amount for the car.
        input_distance (int): distance attempted to move.
        expected_trip_distance (int): expected total distance after move.
        expected_fuel (int): expected remaining fuel after move.

    Logic:
        - Create a Car instance with fixed fuel using patch.
        - Call move() with the given distance.
        - Verify that trip_distance and fuel are updated correctly.
          The car cannot move farther than the remaining fuel.

    Assertions:
        assert c.trip_distance == expected_trip_distance
        assert c.fuel == expected_fuel
    """
    # Create a car and forcefully set fuel.
    with patch("HW_2.main.random.randrange", return_value=input_fuel):
        c = Car("T", "B")
    c.move(input_distance)
    assert c.trip_distance == expected_trip_distance
    assert c.fuel == expected_fuel

def test_multiple_moves_accumulate_trip_distance():
    """
    Test accumulation of trip_distance and fuel reduction 
    across multiple consecutive calls to move().

    Logic:
        - Create a Car instance with starting fuel 6 via patch.
        - Call move(2) → car moves 2 km.
        - Call move(3) → car moves another 3 km.
        - Check trip_distance == 5 and fuel == 1.
        - Call move(5) → only 1 km can be covered due to limited fuel.
        - Check final trip_distance == 6 and fuel == 0.

    Assertions:
        assert c.trip_distance == expected distance after each series of moves
        assert c.fuel == expected remaining fuel after each move
    """
    with patch("HW_2.main.random.randrange", return_value=6):
        c = Car("T", "B")
    c.move(2)
    c.move(3)
    # First two calls: 5 completed, 1 remaining.
    assert c.trip_distance == 5
    assert c.fuel == 1
    c.move(5) # Only 1 can pass.
    assert c.trip_distance == 6
    assert c.fuel == 0

def test_str_represenation():
    """
    Test the string representation of a Car object via __str__().

    Logic:
        - Create a Car instance with fixed fuel using patch.
        - Verify that __str__() returns the string in format "model (color)".

    Assertions:
        assert str(c) == "<model> (<color>)"
    """
    with patch("HW_2.main.random.randrange", return_value=1):
        c = Car("Lexus_RZ", "yellow")
    assert str(c) == "Lexus_RZ (yellow)"

