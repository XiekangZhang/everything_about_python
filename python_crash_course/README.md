# Python Crash Course

this python instruction is based on the book Python crash course 2nd edition by Eric Matthes.

## Part 1

some useful string static methods:

- str.title()
- str.upper()
- str.lower()
- f"{parameter}" / "{}".format(parameter)
- str.rstrip() / str.lstrip() / str.strip()

Python defaults to a float in any operation that uses a float, even if the output is a whole number.

some useful list static methods:

- list[index]
- list.append(one_element)
- list.insert(position, one_element)
- del list[index] / list.pop(optional_index) / list.remove(one_element): only deletes the first occurrence
- list.sort(reverse=True/False): sort list permanently / sorted(list, reverse=True/False): sort list temporarily
- list.reverse()
- len(list)
- list[from:to]: slicing a list, negative number is acceptable
- list.copy() / list[:]

the following list static methods are only for numerical elements

- range(from, to, step) vs. list(range(from, to, step))
- min(list), max(list), sum(list)

some useful dictionary static methods:

- dict.get(key, error_handling_if_key_does_not_exist)
- dict.items() -> (key, value)
- dict.keys()
- dict.values()
- del dict[key]

some other useful standard library:

- from random import randint -> numerical
- from random import choice -> characters

### Data Structure Comparison

- list: changeable collection
- tuple: unmutable collection
- dictionary: key, value pair

### Function

- \*args and \*\*kwargs used for arbitrary arguments in a function

### Classes

- creating an object from a class is called instantiation

### Files and exceptions

- Python can only write strings to a text file.
- open(filename, mode) --> "a": append, "w": write

### Unit Test

- assertEqual(a, b)
- assertnotEqual(a, b)
- assertTrue(x)
- assertFalse(x)
- assertIn(item, list)
- assertNotIn(item, list)
- setUp(self) method
