"""
- Python works by converting your human-readable code into a lower-level format called bytecode, which is then executed by the Python Virtual Machine.
- memory management:
    - everything is an object
    - reference counting: CPython keeps a count for each object of how many variables are referencing it.
    - garbage collection: when the reference count drops to zero, the object is deallocated.
- The Global Interpreter Lock (GIL)
    - a mutex (a type of lock) that ensures only one thread can execute Python bytecode at a time.
    - however, the multiprocessing module could be used to bypass the GIL by running each task in a separate process with its own Python interpreter and memory space.
- use f'{func(xxx) = }' to print the function name and its argument value
- important code snippets:
    - globals()[name] = dataclass(type(name, (object,), {'__annotations__': dict.fromkeys({*common_fields, *fields})})))
        - {*common_fields, *fields} merge two collections into a single set
        - {'__annotations__': ...} creates a dictionary with the keys being the field names and the values being None.
            This is how a dataclass discovers which attributes it needs to manage.
        - type(name, (object,), ...) creates a new class dynamically. (class name, a tuple of base classes, a dictionary of attributes & methods)
        - this final step assigns the newly created dataclass to that dictionary using the name string as the key.
- __build_class__ is the conductor that manages the complex sequence of operations required to build a class
- __init_subclass__ is a special method that allows a parent class to customize its own subclasses at the time of their creation.

- all the interesting stuff happens at python run time, not at compile time
- what compiler do:
    - scope determination - where parameters come from
    - name mangling
    - `super` argument insertion
"""

from __future__ import annotations
from typing import Union
from dis import dis


def f(x, y):
    if __debug__:
        print("debug mode")
    return x + y


# dis(f)


def g(x):
    assert x > 0, "x must be positive"
    return x


# dis(g)


def say_hello_func(self):
    return "Hello"


MyClass = type("MyClass", (object,), {"x": 10, "say_hello": say_hello_func})

# * Lambda functions --> lambda arguments: expression
add_lambda = lambda x, y: x + y


def greet(name: str, excited: bool) -> str:
    if excited:
        return f"Hello, {name}!"
    return f"Hello, {name}."


"""
@lambda f: setattr(
    mod := __import__("builtins"), f.__name__, f(getattr(mod, f.__name__))
)
def test(original_print):
    def new_test(*args, **kwargs):
        original_print("[MODIFIED]", *args, **kwargs)

    return new_test
"""


# Monkey patching example
# cls and self
class Car:
    vehicle_type = "Automobile"

    def __init__(self, color: Union[str, None] = None) -> None:
        self.color = color

    @classmethod
    def get_vehicle_type(cls):
        return f"{cls.vehicle_type = }"

    @classmethod
    def from_config(cls, config):
        return cls(color=config.get("color", "unknown"))

    def drive(self):
        return "Driving normally"


def modified_drive(self):
    return "Driving with modifications"


# __init_subclass__ example
class PluginBase:
    plugins = {}

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        print(f"Registering plugin: {cls.__name__}")
        cls.plugins[cls.__name__] = cls


class PluginA(PluginBase):
    pass


class PluginB(PluginBase):
    pass


# a simple dynamic function dispatcher
import math


class DynamicDispatcher:
    def call_func(self, func_name: str, *args):
        if hasattr(math, func_name):
            func_to_call = getattr(math, func_name)
            return func_to_call(*args)
        else:
            raise ValueError(f"Function {func_name} not found in math module.")


if __name__ == "__main__":
    # print(f"{f.__code__.co_code = }")
    # dis(f, show_caches=True)
    # print(f"{f(123, 456)}")
    m = MyClass()
    print(f"{m.x = }")
    print(f"{m.say_hello() = }")
    print(f"{MyClass.__annotations__ = }")
    print(f"{greet.__annotations__ = }")

    print(f"{add_lambda(3, 4) = }")
    Car.drive = modified_drive
    my_car = Car()
    print(f"{my_car.drive() = }")
    print(f"{Car.get_vehicle_type() = }")
    new_car = Car.from_config({"color": "red"})
    print(f"{new_car.color = }")

    print(f"{PluginBase.plugins = }")

    dispatcher = DynamicDispatcher()
    result = dispatcher.call_func("sqrt", 16)
    print(f"Result of math.sqrt(16): {result}")

    # walrus operator example --> assigns a value to a variable as part of an expression
    results = [y for x in range(10) if (y := x * 2) > 5]
    print(f"{results = }")

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
