# official python tutorial documentation

## Table of contents

- [An Informal Introduction to Python](#an-informal-introduction-to-python)
- [More Control Flow Tools](#more-control-flow-tools)
- [Data Structures](#data-structures)
  - [List, Tuple, Sets](#list-tuple---immutable-sets---no-duplicate-elements)
  - [Looping Techniques](#looping-techniques)
  - [queues](#from-collections-import-deque)
  - [Comparing sequences and other types](#comparing-sequences-and-other-types)
- [Modules](#modules)
- [Error and Exceptions](#errors-and-exceptions)
- [Classes](#classes)
  - [Scopes and Namespace](#scopes-and-namespaces)
  - [Dataclasses](#dataclasses)
  - [Iterators](#iterators)

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

- list.clear(), list.index(x[, start[, end]]), list.count(x)
- list as stacks (last-in, first-out) --> append() with pop()
- set can be defined and initialized with `{1, 2, 3, 4}` or `set(...)`
- seta - setb: elements in a but not in b
- seta | setb: elements in a or in b or both
- seta & setb: elements in both a and b
- seta ^ setb: elements in a or in b but not both

#### Looping Techniques

- dict.items()
- for index, v in enumerate(list)
- for a, b in zip(lista, listb)

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
- a scope is the set of rules for finding which dictionary to look in
  - search order (LEGB: local --> enclosing --> gobal --> built-in)

#### dataclasses

- use `@dataclass` to define a structure like _struct_ in C or java bean

#### iterators

- to implement your own iterators, you have to develop `__iter__()` and `__next__()` function

### Brief Tour of the Standard Libraray

### Brief Tour of the Standard Library - Part II

### Virtual Environments and Packages

### Interactive Input Edition and History Substitution

### Floating-Point Arithmetic: Issues and Limitations

## built-in

#### Text Sequence Type - str (complete it later)

- str.isalnum()
- str.isidentifier(): 1. it cannot be empty. 2. the 1st character must be a letter or an underscore. 3. the rest of the characters must be letters, undersocres, or digits.
- iskeyword(str): Python keywords
- str.swapcase()
- str.ljust(), str.rjust(), str.center()
- f'{a= !a|!r|!s|:.6f}': ascii(), repr(), str() and last 6 digits
- str.maketrans(from, to), <str>.translate(...)
