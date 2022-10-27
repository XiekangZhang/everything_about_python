from random import randint


class Die:
    """A class representing a single dice."""

    def __init__(self, num_sides: int = 6) -> None:
        """Assume a six-sided die."""
        self.num_sides = num_sides

    def roll(self) -> int:
        """Return a random value between 1 and number of sides."""
        return randint(1, self.num_sides)
