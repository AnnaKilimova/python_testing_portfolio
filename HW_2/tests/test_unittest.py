import unittest
from unittest.mock import patch, MagicMock
from ..main import Car

class TestCar(unittest.TestCase):
    """
    TestCase containing unit tests for the Car class.

    Each test is small and focused:
    - test_init:      verifies constructor behavior and default state.
    - test_move_*:    verifies move behavior when requested distance is less/equal/more than fuel.
    - test_multiple_moves: verifies state after multiple sequential moves.
    - test_str:       verifies __str__ / string representation.

    Mocking:
    - Randomness in Car initialization is controlled by patching
      `HW_2.main.random.randrange` so the initial `fuel` is deterministic in tests.
    """
    @patch("HW_2.main.random.randrange", return_value=4)
    def test_init(self, mock_rand: MagicMock) -> None:
        """
        Test Car initialization.

        Behavior under test:
        - The Car constructor obtains an initial `fuel` by calling `random.randrange`.
        - With `random.randrange` patched to return 4, the Car should be created
          with 4 units of fuel.

        Assertions:
        - model and color are set from constructor arguments,
        - fuel equals the patched value (4),
        - trip_distance is initialized to 0.

        Args:
            mock_rand: the MagicMock instance that replaced random.randrange.
        """
        c = Car("BMW_X6", "white")
        self.assertEqual(c.model, "BMW_X6")
        self.assertEqual(c.color, "white")
        self.assertEqual(c.fuel, 4)
        self.assertEqual(c.trip_distance, 0)

    @patch("HW_2.main.random.randrange", return_value=5)
    def test_move_less_than_fuel(self, mock_rand: MagicMock) -> None:
        """
        Test moving a distance smaller than available fuel.

        Setup:
        - Car starts with 5 units of fuel (patched).
        Action:
        - Move the car by 3 units.
        Expected:
        - trip_distance increases by 3,
        - remaining fuel is reduced by 3 (5 -> 2).

        Args:
            mock_rand: the MagicMock instance that replaced random.randrange.
        """
        c = Car("T", "B")
        c.move(3)
        self.assertEqual(c.trip_distance, 3)
        self.assertEqual(c.fuel, 2)

    @patch("HW_2.main.random.randrange", return_value=5)
    def test_move_more_than_fuel(self, mock_rand: MagicMock) -> None:
        """
        Test moving a distance greater than available fuel.

        Setup:
        - Car starts with 5 units of fuel (patched).
        Action:
        - Request move of 10 units.
        Expected:
        - The car can only travel as far as the available fuel allows (5),
        - trip_distance becomes 5,
        - fuel becomes 0.

        Args:
            mock_rand: the MagicMock instance that replaced random.randrange.
        """
        c = Car("T", "B")
        c.move(10)
        self.assertEqual(c.trip_distance, 5)
        self.assertEqual(c.fuel, 0)
    
    @patch("HW_2.main.random.randrange", return_value=5)
    def test_move_equal_to_fuel(self, mock_rand: MagicMock) -> None:
        """
        Test moving a distance exactly equal to available fuel.

        Setup:
        - Car starts with 5 units of fuel (patched).
        Action:
        - Move the car by exactly 5 units.
        Expected:
        - trip_distance becomes 5,
        - fuel becomes 0.

        Args:
            mock_rand: the MagicMock instance that replaced random.randrange.
        """
        c = Car("T", "B")
        c.move(5)
        self.assertEqual(c.trip_distance, 5)
        self.assertEqual(c.fuel, 0)

    @patch("HW_2.main.random.randrange", return_value=2)
    def test_multiple_moves(self, mock_rand: MagicMock) -> None:
        """
        Test multiple sequential moves and fuel consumption.

        Setup:
        - Car starts with 2 units of fuel (patched).
        Actions:
        - Move 1 unit, then move 2 units.
        Expected:
        - First move reduces fuel to 1 and increases trip_distance by 1.
        - Second move can only move the remaining 1 unit (not 2) because fuel is insufficient.
        - Final trip_distance is 2 and fuel is 0.

        Args:
            mock_rand: the MagicMock instance that replaced random.randrange.
        """
        c = Car("T", "B")
        c.move(1)
        c.move(2) 
        self.assertEqual(c.trip_distance, 2)
        self.assertEqual(c.fuel, 0)

    @patch("HW_2.main.random.randrange", return_value=3)
    def test_str(self, mock_rand: MagicMock) -> None:
        """
        Test string representation of Car.

        Behavior:
        - str(car) should return "<model> (<color>)".
        - This is purely formatting; initial fuel value is irrelevant to the assertion,
          but we patch randomness for consistency.

        Args:
            mock_rand: the MagicMock instance that replaced random.randrange.
        """
        c = Car("Lexus_RZ", "yellow")
        self.assertEqual(str(c), "Lexus_RZ (yellow)")


    