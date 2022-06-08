class Battery:
    """A simple attempt to model a battery for an electric car."""
    def __init__(self, battery_size=75):
           """Initialize the battery's attributes."""
           self.battery_size = battery_size

    def describe_battery(self):
           """Print a statement describing the battery size."""
           print(f"This car has a {self.battery_size}-kWh battery.")