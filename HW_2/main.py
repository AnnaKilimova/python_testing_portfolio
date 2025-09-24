import random

class Car:
    """
    A class to represent a car in a race.

    Attributes:
        model (str): The model of the car.
        color (str): The color of the car.
        fuel (int): The amount of fuel the car has (initially set randomly from 0 to 8).
        trip_distance (int): The total distance travelled by the car.

    Methods:
        move(distance): Moves the car by the given distance, decreasing fuel accordingly.
    """
    def __init__(self, model: str, color: str) -> None:
        """    
        Initializes a Car object with a model, color, random fuel level, and trip distance set to 0.

        Args:
            model (str): The model of the car.
            color (str): The color of the car.
        """
        self.fuel = random.randrange(0, 8)
        self.trip_distance = 0
        self.model = model
        self.color = color

    def move(self, distance: int) -> None:
        """
        Moves the car by a specified distance, reducing fuel accordingly.

        If the requested distance is greater than the available fuel, the car will move only
        as far as the remaining fuel allows. After moving, fuel is reduced by the distance travelled.

        Args:
            distance (int): The distance the car is attempted to move.

        Returns:
            None
        """
        if distance > self.fuel:
            distance = self.fuel
        self.trip_distance += distance
        self.fuel -= distance
    

    def __str__(self) -> str:
        """
        Returns a string representation of the car.

        Returns:
            str: A string in the format "model (color)".
        """
        return f"{self.model} ({self.color})"
    

car_1 = Car("BMW_X6", "white")
car_2 = Car("Lexus_RZ", "yellow")
car_3 = Car("ToyotaCamry_VVT-h", "black")

cars = [car_1, car_2, car_3]

desired_dist = 12
race_dist = 0
winner = None

while race_dist < desired_dist:
    # Checking if there's even one car with fuel.
    if all(car.fuel <= 0 for car in cars):
        print("The race has been stopped: everyone has run out of fuel.")
        break

    for car in cars:
        distance = random.randrange(0, 9)
        car.move(distance)

        if car.trip_distance >= desired_dist:
            winner = car
            race_dist = desired_dist 
            break

if winner:
    print(f"The winner: {winner.model}, distance {winner.trip_distance} km.")
else:
    print("\nNo one reached the destination.")

print("\n--- Race results. ---")
for car in cars:
    print(f"{car}: distance = {car.trip_distance}, fuel = {car.fuel}")


# Note: According to the original problem statement:
# Each car's fuel is randomly 0–8 and movement per turn is 0–8.
# The winner is declared when a car reaches or exceeds desired_dist.
# With these parameters, it is possible that all cars run out of fuel 
# before reaching desired_dist, so a winner is not guaranteed.
# To ensure a winner, either increase the initial fuel range or 
# define the winner as the car that traveled the farthest if all stop early.
