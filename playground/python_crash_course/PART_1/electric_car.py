from car import Car
from battery import Battery

class ElectricCar(Car):
    """Represent aspects of a car, specific to electric vehicles.

    Args:
        Car (_type_): _description_
    """
    def __init__(self, make, model, year):
        """Initialize attributes of the parent class.

        Args:
            make (_type_): _description_
            model (_type_): _description_
            year (_type_): _description_
        """
        super().__init__(make, model, year)
        #self.battery_size = 75
        self.battery = Battery()

    def describe_battery(self):
        print(f"This car has a {self.battery_size}-kWh battery")

    def fill_gas_tank(self):
        print("This car doesn't need a gas tank!")

if __name__ == "__main__":
    my_tesla = ElectricCar("tesla", "model s", 2019)
    print(my_tesla.get_descriptive_name())
    #my_tesla.describe_battery()
    my_tesla.battery.describe_battery()
    my_tesla.fill_gas_tank()