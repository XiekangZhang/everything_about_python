Table of contents:

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [official python tutorial documentation](#official-python-tutorial-documentation)
  - [Python 3.13.x](#python-313x)
    - [An Informal Introduction to Python](#an-informal-introduction-to-python)
    - [More Control Flow Tools](#more-control-flow-tools)
    - [Data Structures](#data-structures)
      - [List (Tuple - immutable, Sets - no duplicate elements)](#list-tuple---immutable-sets---no-duplicate-elements)
      - [Looping Techniques](#looping-techniques)
      - [from collections import deque](#from-collections-import-deque)
      - [comparing sequences and other types](#comparing-sequences-and-other-types)
    - [Modules](#modules)
      - [The Module Search Path](#the-module-search-path)
    - [Input and Output](#input-and-output)
    - [Errors and Exceptions](#errors-and-exceptions)
    - [Classes](#classes)
      - [Scopes and Namespaces](#scopes-and-namespaces)
      - [dataclasses](#dataclasses)
      - [iterators](#iterators)
  - [The Python Standard Library](#the-python-standard-library)
    - [Built-in Functions](#built-in-functions)
      - [classmethod, staticmethod](#classmethod-staticmethod)
      - [mode variants within open](#mode-variants-within-open)
      - [property, setter, deleter](#property-setter-deleter)
      - [dynamic import](#dynamic-import)
    - [Built-in Types](#built-in-types)
      - [truth value testing](#truth-value-testing)
      - [boolean operations](#boolean-operations)
      - [sequence types - list, tuple, range](#sequence-types---list-tuple-range)
        - [list](#list)
        - [range](#range)
      - [string methods](#string-methods)
        - [printf-style String Formatting](#printf-style-string-formatting)
      - [binary sequence types - bytes, bytearray, memoryview](#binary-sequence-types---bytes-bytearray-memoryview)
        - [bytes - same operations with str](#bytes---same-operations-with-str)
        - [bytearray - same operations with str](#bytearray---same-operations-with-str)
        - [memory views](#memory-views)

<!-- /code_chunk_output -->

# official python tutorial documentation

## Python 3.13.x

### An Informal Introduction to Python

- division (/) always returns a float.
- use `//` to get an integer (floor division) and `%` to calculate the remainder
- use `j` suffix to indicate that a number is complex number
- `\` is interpreted as escape mark. If you don't want `\` to be as a special characters, you can add `r<...\>` prefix to refer that the given string should be treated as raw string
- Python strings cannot be changed - they are immutable. Therefore, assigning to an indexed position in the string results in an error.

### More Control Flow Tools

- **else** Clauses on Loops: In a `for` loop, the `else` clause is executed after the loop finishes its final iteration, that is, if no break occurred.
- **match** ... **case**
- the default value in a function is evaluated only once. If you define it as a mutable object, it will be e.g., appended.
- in function you can use '/' or '_' to define what kind of parameter will be used. `def f(pos1, pos2, /, pos_or_kwd, _, kwd1, kwd2)`
- arbitrary argument: `def f(*args, **kwargs)`
- function `__annotations__` are completely optional metadata information about the types used by user-defined functions

### Data Structures

#### List (Tuple - immutable, Sets - no duplicate elements)

- `list.clear()`, `list.index(x[, start[, end]])`, `list.count(x)`
- list as stacks (last-in, first-out) --> append() with pop()
- set can be defined and initialized with `{1, 2, 3, 4}` or `set(...)`
- seta `-` setb: elements in a but not in b
- seta `|` setb: elements in a or in b or both
- seta `&` setb: elements in both a and b
- seta `^` setb: elements in a or in b but not both

#### Looping Techniques

- `dict.items()`
- `for index, v in enumerate(list)`
- `for a, b in zip(lista, listb)`

#### from collections import deque

- queues (first-in, first-out) --> `deque` append() with popleft()

#### comparing sequences and other types

- The comparison uses lexicographical ordering: first the first two items are compared, and if they differ this determines the outcome of the comparison; if they are equal, the next two items are compared, and so on, until either sequence is exhausted

### Modules

- you can use the `-O` or `-OO` switches on the Python command to reduce the size of a compiled module.
- `dir(<func>)` is used to find out which names a module defines.

  ```python
  # __init__.py: treat directories containing the file as packages
  __all__ = ['echo', 'surround', 'reverse', 'something_new'] # import the three named submodules, if from sound.effects import * is used.

  def something_new():
    pass
  ```

#### The Module Search Path

- sys.builtin_module_names
- sys.path
  - the directory containing the input script
  - _PYTHONPATH_
  - _site-packages_ within _site_ module

### Input and Output

- `print(f"something{...!a|!s|!r}")`: `!a`: `ascii()`, `!s`: `str()`, `!r`: `repr()`
- the `=` specifier can be used to expand an expression to the text of the expression, an equal sign, then the representation of the evaluated expression

```python
bugs = 'roaches'
count = 13
area = 'living room'
print(f"Debugging {bugs=} {count=} {area=}")
```

- `str.rjust()`, `str.ljust()`, `str.center()`, and `str.zfill()`

```python
import json
x = [1, 'simple', 'list']
json.dumps(x)
```

### Errors and Exceptions

- `error.add_note(...)` to add additional information to defined exception
- `try...except...else...finally...` `else` will be run if no error exists and `finally` always run

### Classes

#### Scopes and Namespaces

- a namespace is a dictionary mapping names to objects
  - Python creates several namespaces as a program runs:
    - built-in > global (module) > local (function / class)
  - `globals()` and `locals()` return the current global and local namespace respectively
- a scope is the set of rules for finding which dictionary to look in
  - search order (LEGB: local --> enclosing --> gobal --> built-in)

#### dataclasses

- use `@dataclass` to define a structure like _struct_ in C or java bean

#### iterators

- to implement your own iterators, you have to develop `__iter__()` and `__next__()` function

## The Python Standard Library

### Built-in Functions

#### classmethod, staticmethod

- a `@classmethod` is a decorator in Python that defines a method bound to the class, not the instance of the class.
  - 1st argument: `cls`
  - primary use case: factory methods that create instances
- a `@staticmethod` is a decorator in Python that defines a method unbound to the class nor the instance of the class.
  - no needing of `cls` nor `self`
  - primary use case: utility functions that are related to the class

#### mode variants within open

- `open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)`

  | mode | meaning                                                         |
  | :--- | :-------------------------------------------------------------- |
  | 'r'  | open for reading                                                |
  | 'w'  | open for writing, truncating the file first                     |
  | 'x'  | open for exclusive creation, failing if the file already exists |
  | 'a'  | open for writing, appending to the end of file if it exists     |
  | 'b'  | binary mode                                                     |
  | 't'  | text mode                                                       |
  | '+'  | open for updating (reading and writing)                         |

#### property, setter, deleter

- `@property` (getter) + `@<property>.setter` + `@<property>.deleter`: similar to java private parameter + public getter and setter

#### dynamic import

- `__import__(<module_name>)` and `importlib.import_module(<module_name>)` can be used for dynamic imports & metaprogramming

### Built-in Types

#### truth value testing

- the built-in objects are considered `False`:
  - constants defined to be false: `None` and `False`
  - zero of any numeric type: `0`, `0.0`, `0j`, `Decimal(0)`, `Fraction(0, 1)`
  - empty sequences and collections: `''`, `()`, `{}`, `set()`, `range(0)`

#### boolean operations

- `and`, `or` are short-circuit operator
- `not` has a lower priority than non-Boolean operators, so `not a == b` is interpreted as `not (a == b)`

#### sequence types - list, tuple, range

##### list

- list constructor: `list('abc')` returns `['a', 'b', 'c']` and `list((1, 2, 3))` returns `[1, 2, 3]`
- sort method sorts the list in place, using only `<` comparisons between items

##### range

- in comparison to the memory usuage, `range` has much more memory efficiency than `list` and `tuple`.

#### string methods

- `iskeyword(str)`, `str.capitalize()`, `str.center(width[, fillchar])`, `str.count(sub[, start[, end]])`, `str.encode(encoding='uft-8', erros='strict')`, `str.expandtabs(tabsize=)`, `str.find(sub[, start[, end]])`, `str.format(*args, **kwargs)`, `str.format_map(mapping, /)`, `str.index(sub[, start[, end]])`, `str.isascii()`, `str.isdecimal()`, `str.isdigit()`, `str.isidentifier()`, `str.islower()`, `str.isnumeric()`, `str.isprintable()`, `str.isspace()`, `str.istitle()`, `str.isupper()`, `str.join(iterable)`, `str.ljust(width[, fillchar])`, `str.removeprefix(prefix, /)`, `str.removesuffix(suffix, /)`, `str.replace(old, new, count=-1)`, `str.rjust(width[, fillchar])`, `str.rsplit(sep=None, maxsplit=-1)`, `str.split(sep=None, maxsplit=-1)`, `str.splitlines(keepends=False)`, `str.startswith(prefix[, start[, end]])`, `str.title()`, `str.upper()`, `str.zfill(width)`
- `str.endswith(suffix[, start[, end]])`: suffix could be a tuple meaning either or
- `str.casefold()`: similar to lower() but remove all case distinctions
- `str.isalnum()`: return `True` if all characters in the string are alphanumeric and there is at least one character
- `str.isalpha()`: return `True` if all characters in the string are alphabetic and there is at least one character
- `str.lstrip([chars])`: removes any combination of the chars from the beginning of the string until it encounters a character that is not in the set if chars is given other empty characters from left side are removed, similar to `str.rstrip([chars])` and `str.strip([chars])`
- `str.partition(sep)`: returns `(before, sep, after)`, similar with `str.rpartition(sep)`
- `str.rfind(sub[, start[, end]])`: returns the highest index in the string where substring sub is found, similar to `str.rindex(sub[, start[, end]])` but raise error if not found
- `str.swapcase()`: string with uppercase characters converted to lowercase and vice versa
- `f'{a= !a|!r|!s|:.6f}'`: `ascii()`, `repr()`, `str()` and last 6 digits
- `str.maketrans(from, to)`, `str.translate(table)`

##### printf-style String Formatting

- the conversion flag characters are:

| Flag | Meaning                                                                                         |
| ---- | ----------------------------------------------------------------------------------------------- |
| '#'  | the value conversion will use the 'alternate form'                                              |
| '0'  | the conversion will be zero padded for numeric values                                           |
| '-'  | the converted value is left adjusted (overrides the '0' conversion if both are given)           |
| ' '  | a blank should be left before a positive number or empty string produced by a signed conversion |
| '+'  | a sign character will precede the conversion                                                    |

- the conversion types are:
  - `'d'`, `'i'`, `'o'`, `'u'`, `'x'`, `'X'`, `'e'`, `'E'`, `'f'`, `'F'`, `'g'`, `'G'`, `'c'`, `'r'`, `'s'`, `'a'`, `%`

#### binary sequence types - bytes, bytearray, memoryview

##### bytes - same operations with str

- `bytes([source[, encoding[, errors]]])`: `b'string'`, `bytes.fromhex('...')`, `b'string'.hex([sep[, bytes_per_sep]])`

##### bytearray - same operations with str

- `bytearray(b'Hi!')`, `bytearray.fromhex('...')`, `bytearray(b'string').hex()`

##### memory views
