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
- By default, instances of user-defined classes are considered truthy, unless either ```__bool__``` or ```__len__```is
implemented. Basically, _bool(x)_ calls ```x.__bool__()```. If ```__bool__``` is not implemented, Python tries to invoke
```x.__len__()```.
- a _metaobject protocal_ is a fancy synonym for object model: an API for core language constructs.

### Important feature
- ``collections.namedtuple(subclass_name, constructor)``
- ``__getitem__(self, position)`` to enable the custom collections to support slicing & iterable &
``in`` constraint
- ``random.choice(iter)``
- ``f"{value!s/r/a}"`` ! means format: _s => str(), r => repr(), a => ascii()_
- ``__repr__(self)`` keeps the object, usually for debugging and logging
``__str__(self)`` converts everything to string, it calls ``print()`` function, usually for presentation to end users.

## Chapter 2: An Array of Sequences
- The standard library offers a rich selection of sequence types implemented in C.
  - Container sequences (list, tuple, collections.deque, etc.) vs Flat sequences (str, bytes, array.array, etc.)
  - Mutable sequences (list, bytearray, array.array, collections.deque, etc.) vs Immutable sequences (tuple, str, bytes, etc.)
- Every Python object in memory has a header with metadata. 
  - a float, has a value field and two metadata fields, on a 64-bit Python build, each of those fields takes 8 bytes.
    - ``ob_refcnt``: the object's reference count
    - ``ob_type``: a pointer to the object's type
    - ``ob_fval``: a C double holding the value of the float 

### List Comprehensions and Generator Expressions
- If you are not doing something with the produced list, you should not use listcomp. To initialize tuples, arrays,
and other types of sequences you could use genexp.
- The genexp yields items one by one. It is useful to produce output that you don't need to keep in memory.
- ```:=```: walrus operator: remain accessible after listcomp or expressions return (no _global_, or _nonlocal_ declaration)
- * treats list with individual element

### Tuples are not just immutable lists
- Tuples hold records: each item in the tuple holds the data for field, and the position of the item gives its meaning.
- Tuples as immutable lists: clarity & better performance.
- Tuples with mutable items can be a source of bugs. An object is only hashable if its value cannot ever change. 
- % treats tuple with individual element

### Unpacking Sequences and Iterables
- ```[record] = query_returning_single_row() or (record,)```
- ``[[field]] = query_returning_single_row_with_single_field() or ((field,),)``

### Pattern Matching with Sequences
- _match/case_: _str_, _bytes_, and _bytearray_ are not handled as sequences in the context of _match/case_.
- _type(var)_ in _case_ will perform a runtime type check.

### Slicing