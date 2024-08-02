class Dog:
    """A simple attempt to model a dog.
    """

    def __init__(self, name, age) -> None:
        """Initialize name and age attributes. --> Java Constructor

        Args:
            name (_type_): _description_
            age (_type_): _description_
        """
        self.name = name
        self.age = age

    def sit(self) -> None:
        """Simulate a dog sitting in response to a command.
        """
        print(f"{self.name}is now sitting.")

    def roll_over(self) -> None:
        """Simulate rolling over in response to a command.
        """
        print(f"{self.name} rolled over!")

if __name__ == "__main__":
    my_dog = Dog("Willie", 6)
    print(f"My dog's name is {my_dog.name}.")
    print("My dog is {} years old.".format(my_dog.age))
    my_dog.sit()
    my_dog.roll_over()