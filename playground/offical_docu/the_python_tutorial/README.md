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
- in function you can use '/' or '*' to define what kind of parameter will be used. `def f(pos1, pos2, /, pos_or_kwd, *, kwd1, kwd2)`
- arbitrary argument: `def f(*args, **kwargs)`
- function `__annotations__` are completely optional metadata information about the types used by user-defined functions

### Data Structures

#### List (Tuple, Sets)

- list.clear(), list.index(x[, start[, end]]), list.count(x)
- list as stacks (last-in, first-out) --> append() with pop()
- seta - setb, seta | setb, seta & setb, seta ^ setb

#### Looping Techniques

- dict.items()
- for index, v in enumerate(list)
- for a, b in zip(lista, listb)

#### from collections import deque

- queues (first-in, first-out) --> append() with popleft()

### Modules

- you can use the `-O` or `-OO` switches on the Python command to reduce the size of a compiled module.
- `dir(<func>)` is used to find out which names a module defines.
- importing \* from a package

  ```python
  # __init__.py
  __all__ = ['echo', 'surround', 'reverse', 'something_new'] # import the three named submodules

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

```python
import json
x = [1, 'simple', 'list']
json.dumps(x)
```

### Errors and Exceptions

### Classes

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
