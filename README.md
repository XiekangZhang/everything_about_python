# everything_about_python

pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip install -U

conda update --all

conda env update --name myenv --file local.yml --prune

conda env create -n env_name --file local.yml
conda activate env_name
conda deactivate
conda remove -n env_name --all

## IT terminology - concurrency & parallelism

### Concurrent vs. Parallel

- **Concurrency**: deals with managing multiple tasks at once
- **Parallelism**: deals with executing multiple tasks at the exact same instant

A system can be _concurrent_ without being _parallel_ (e.g., a single-core CPU rapidly switching between tasks). A system that is parallel is inherently concurrent.

### why is concurrency important in IT?

- Responsiveness: concurrency allows the UI to remain responsive
- Resource Utilization: concurrency allows the CPU to do other work while one task is waiting, rather than sitting idle
- Throughput: concurrency allows the server to process multiple requests without one blocking others
- Modularity: breaking down complex problems into smaller, independent tasks that can be managed concurrently

## functools - higher-order functions and operations on callable objects

- the _functools_ module is for higher-order functions: functions that act on or return other functions.

## metaprogramming

- metaprogramming is the technique of writing code that can inspect, modify, or generate other code as it runs. In essence, it's the practice of writing programs that treat other programs as their data.
- common metaprogramming techniques in Python
  - decorators
  - metaclasses
  - type hinting and inspection: `type()` and `inspect`
  - dynamic code execution: `exec()` and `eval()`
- key techniques for dynamic programming
  - **introspection**: this is the ability to examine an object's type and properties at runtime. `getattr(obj, 'attr_name')`, `setattr(obj, 'attr_name', value)`, `hasattr(obj, 'attr_name')` and `inspect` module
  - **dynamic code execution**: `eval()`: executes a single expression and returns the result. `exec()`: executes a block of statements. `__import__()`: imports a module using a string name, allowing you to load modules programmatically
  - **dynamic class creation**: you can create new classes without using the `class` keyword by using the `type()` constructor.
  - **decorators and metaclasses**
- usecases:
  - frameworks and ORMs
  - code generation from Schemas
  - metaclasses
- TODOS:
  - - [X]: Master the Basics: Functions as First-Class Objects
  - - [ ]: Learn Introspection with Built-in functions
  - - [ ]: Implement Decorators
  - - [ ]: Understand Dynamic Class Creation with `type()`
  - - [ ]: Dive into Metaclasses: A metaclass defines the rules for creating a class. Understanding them helps you see how `__build_class__` and `type()` work together.
      - key methods to learn: `__new__` and `__init__` on the metaclass, and `__prepare__`
  - - [ ]: descriptors are objects that control attribute access, like `@property`, `staticmethod`, `classmethod`, `__get__`, `__set__`, `__delete__`

### Monkey patching

- Monkey patching is the practice of dynamically modifying or replacing code (like functions, methods, or classes) at runtime. Instead of changing the source code of a library, you apply changes to it while your program is running.
- usecases:
  - testing
  - bug fixes
  - extending behavior

## import

- when a Python file is imported into another script, the interpreter executes the entire file from top to bottom. If you have executable code - like function calls, print statements, or code that starts a process - at the top level, it will run immediately.
  - solution: `if __name__ == '__main__'`
- `import math`: **later bound** vs `from math import pi`: **early bound**

## variables scope

- **LEGB** rule: Local, Enclosing, Global, Built-in
