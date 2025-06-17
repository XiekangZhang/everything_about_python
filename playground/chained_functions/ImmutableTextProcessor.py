"""
one example of chained functions, also called method chaining or fluent interfaces.
this script focuses on immutable method chaining

Limitations: immutable object is better for tracking, but it can be less efficient if you're performing many operations

@author: XZhang
@version: 0.0.1
@since: 17.06.2025
@dependencies: python==3.12.0
@keywords: fluent interfaces, immutable, better tranking less performing
"""


class ImmutableTextProcessor:
    def __init__(self, text=""):
        self.text = text

    def to_uppercase(self):
        return ImmutableTextProcessor(self.text.upper())  # Return a new object

    def to_lowercase(self):
        return ImmutableTextProcessor(self.text.lower())

    def remove_whitespace(self):
        return ImmutableTextProcessor(self.text.strip())

    def replace(self, old, new):
        return ImmutableTextProcessor(self.text.replace(old, new))

    def get_text(self):
        return self.text


if __name__ == "__main__":
    # Usage:
    processor = ImmutableTextProcessor("     Hello World!  ")
    new_processor = (
        processor.remove_whitespace()
        .to_lowercase()
        .replace("world", "Python")
        .to_uppercase()
    )
    result = new_processor.get_text()
    print(result)  # Output: PYTHON!

    print(processor.get_text())  # Output:   Hello World!  (original object unchanged)
