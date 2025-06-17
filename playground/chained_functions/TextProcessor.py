"""
one example of chained functions, also called method chaining or fluent interfaces.
this script focuses on mutable method chaining

@author: XZhang
@version: 0.0.1
@since: 17.06.2025
@dependencies: python==3.12.0
@keywords: fluent interfaces, object modified, hard to debug
"""


class TextProcessor:
    def __init__(self, text=""):
        self.text = text

    def to_uppercase(self):
        self.text = self.text.upper()
        return self  # important part

    def to_lowercase(self):
        self.text = self.text.lower()
        return self

    def remove_whitespace(self):
        self.text = self.text.strip()
        return self

    def replace(self, old, new):
        self.text = self.text.replace(old, new)
        return self

    def get_text(self):
        return self.text


if __name__ == "__main__":
    processor = TextProcessor("    Hello World!   ")
    result = (
        processor.remove_whitespace()
        .to_lowercase()
        .replace("world", "Python")
        .to_uppercase()
        .get_text()
    )
    print(result)
