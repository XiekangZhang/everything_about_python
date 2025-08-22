import importlib


class Pizza:
    def __init__(self, ingredients) -> None:
        self.ingredients = ingredients

    # Regular instance method
    def display(self) -> None:
        print(f"This pizza has: {self.ingredients}")

    # Class method - a factory
    @classmethod
    def margherita(cls):
        return cls(["mozzarella", "tomatoes"])

    # Static method - a utility
    @staticmethod
    def is_vegetarian(ingredients):
        return all(i not in ["ham", "salami"] for i in ingredients)


class TemperatureConverter:
    def __init__(self, celsius) -> None:
        self._celsius = celsius

    @property
    def celsius(self):
        print("Getting value...")
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        print(f"Setting value to {value}")
        if value < -273.15:
            raise ValueError("Temperature cannot be below absolute zero.")
        self._celsius = value

    @celsius.deleter
    def celsius(self):
        print("Deleting value...")
        del self._celsius


if __name__ == "__main__":
    # using class method
    my_pizza = Pizza.margherita()

    # using the instance method
    my_pizza.display()

    # using the static method
    ingredients_list = ["mozzarella", "mushrooms", "peppers"]
    print(f"Are these ingredients vegetarian? {Pizza.is_vegetarian(ingredients_list)}")

    temp = TemperatureConverter(10)
    print(f"The temperature is {temp.celsius} C.")

    temp.celsius = 25
    try:
        temp.celsius = -300
    except ValueError as e:
        print(f"Error: {e}")

    del temp.celsius

    ###############
    # __import__()#
    ###############
    module_name_to_load = "math"
    old_way_module = __import__(module_name_to_load)
    print(f"Old way: {old_way_module.sqrt(16)}")

    modern_way_module = importlib.import_module(module_name_to_load)
    print(f"Modern way: {modern_way_module.sqrt(16)}")
