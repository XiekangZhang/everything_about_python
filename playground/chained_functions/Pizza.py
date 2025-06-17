"""
one example of chained functions, also called method chaining or fluent interfaces.
this script focuses on builder pattern

@author: XZhang
@version: 0.0.1
@since: 17.06.2025
@dependencies: python==3.12.0
@keywords: builder pattern, fluent interfaces, initiail with multiple parameters
"""


class Pizza:
    def __init__(self, size, crust, toppings):
        self.size = size
        self.crust = crust
        self.toppings = toppings

    def __str__(self):
        return f"Pizza: size={self.size}, crust={self.crust}, toppings={', '.join(self.toppings)}"


class PizzaBuilder:
    def __init__(self) -> None:
        self.size = "medium"
        self.crust = "thin"
        self.toppings = []

    def set_size(self, size):
        self.size = size
        return self

    def set_crust(self, crust):
        self.crust = crust
        return self

    def add_toppings(self, toppings):
        self.toppings.append(toppings)
        return self

    def build(self):
        return Pizza(self.size, self.crust, self.toppings)


if __name__ == "__main__":
    builder = PizzaBuilder()
    my_pizza = (
        builder.set_size("large")
        .set_crust("deep dish")
        .add_toppings("pepperoni")
        .add_toppings("mushrooms")
        .build()
    )
    print(my_pizza)
