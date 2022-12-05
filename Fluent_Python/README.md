# Fluent Python
## Chapter 1. The Python Data Model
- Dunder/magic method: method with double underscore before and after
- Pythonic code is a core skill for Python developers
- ```__len__``` & ``__getitem__`` make a class behaves like a standard Python sequence, allowing it to
benefit from core language features (e.g., iteration and slicing) and from the standard library
- The interpreter takes a shortcut when dealing for built-in types like _list_, _str_, _bytearray_, or
extensions like the _NumPy_ arrays. Python variable-sized collections written in C include a struct 
called _PyVarObject_, which has an _ob_size_ field holding the number of items in the collection. It is 
much faster than calling a method. 
- Normally, your code should not have many direct calls to special methods. If you need to invoke a special
method, it is usually better to call the related built-in function (e.g., len, iter, str, etc.).
- The _abs_ built-in function returns the absolute value of integers and floats, and the magnitude of _complex_ numbers.

### Important feature
- ``collections.namedtuple(subclass_name, constructor)``
- ``__getitem__(self, position)`` to enable the custom collections to support slicing & iterable &
``in`` constraint
- ``random.choice(iter)``
- ``f"{value!s/r/a}"`` ! means format: _s => str(), r => repr(), a => ascii()_
- ``__repr__(self)`` keeps the object ``__str__(self`` converts everything to string, it calls ``print()`` function