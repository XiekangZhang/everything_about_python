"""
- Python works by converting your human-readable code into a lower-level format called bytecode, which is then executed by the Python Virtual Machine.
- memory management:
    - everything is an object
    - reference counting: CPython keeps a count for each object of how many variables are referencing it.
    - garbage collection: when the reference count drops to zero, the object is deallocated.
- The Global Interpreter Lock (GIL)
    - a mutex (a type of lock) that ensures only one thread can execute Python bytecode at a time.


- in cpython, everything is a bytecode
- all python code is executable
- all the interesting stuff happens at python run time, not at compile time
- what compiler do:
    - scope determination - where parameters come from
    - name mangling
    - `super` argument insertion
- global tag is only a hint

"""

from dis import dis


def f(x, y):
    if __debug__:
        print("debug mode")
    return x + y


dis(f)


def g(x):
    assert x > 0, "x must be positive"
    return x


dis(g)


if __name__ == "__main__":
    print(f"{f.__code__.co_code = }")
    dis(f, show_caches=True)
    print(f"{f(123, 456)}")


"""
Metaprogramming is the practice of writing code that manipulates or generate code.
good idea:
if xxx:
    def f_linux():
        pass
else:
    import other_module
    def f_windows():
        pass
f = f_linux if xxx else f_windows

but it is not a good idea in class structure:
1. in dataclasses, you should avoid duplicating fields --> subclasses or other classes or object construction
   common_fields = {'ident', 'user', 'timestamp', 'token'}
   message_types = {
    'DataUpdated': {'update'},
    'DataRemoved': {*()},
    'DataCreated': {'payload'}
   }
   from dataclasses import dataclass
   for name, fields in message_types.items():
    globals()[name] = dataclass(type(name, (object,), {'__annotations__': dict.fromkeys({*common_fields, *fields})})))


    methods = {'f': 'eff', 'g': 'gee', 'h': 'aitch'}
    class T:
        for nm, rv in methods.items():
            locals()[nm] = lambda self, rv=rv: rv

2. in python __method__ can not be created dynamically, thus you have to use type
    class TMeta(type):
        def __call__(self):
            print(f'TMeta.__call__({self!r})')
    class T(metaclass=TMeta):
        def __init__(self):
            print(f'T.__init__({self!r})')
        def __call__(self):
            print(f'T.__call__({self!r})')

3. do not use ABC standard library, use metaclass instead
4. metagrogramming limits: inheritance --> should not be specified and grouped the classes
5. a new way to implement parent and child classes
    class Message:
        @classmethod
        def from_json(cls, json_data):
            yield cls.MESSAGE_TYPES[msg.pop('type')](**msg)
        def __init_subclass__(cls, *, json_key, fields):
            for x in fields:
                cls.__annotations__[x] = None
            cls.MESSAGE_TYPES[json_key] = cls

    @dataclass
    class MessageA(Message, json_key='aaa', fields={'x'}):
        pass
    @dataclass
    class MessageB(Message, json_key='bbb', fields={'y', 'z'}):
        pass
    json_payload = [
        {'type': 'aaa', 'x': 42},
        {'type': 'bbb', 'y': 1, 'z': 2}
    ]
6. what happens with import: it does not execute the code --> do not use executables code in your modules
    import math # late bound --> math.pi
    from math import pi # early bound
    --> from sys import modules --> math = modules['math']
"""
