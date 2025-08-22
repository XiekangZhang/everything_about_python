## markdown

### picture

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://user-images.githubusercontent.com/25423296/163456776-7f95b81a-f1ed-45f7-b7ab-8fa810d529fa.png">
  <source media="(prefers-color-scheme: light)" srcset="https://user-images.githubusercontent.com/25423296/163456779-a8556205-d0a5-45e2-ac17-42d089e3c3f8.png">
  <img alt="Shows an illustrated sun in light mode and a moon with stars in dark mode." src="https://user-images.githubusercontent.com/25423296/163456779-a8556205-d0a5-45e2-ac17-42d089e3c3f8.png">
</picture>

### collapsed section

<details open>
<summary>my test</summary>

| Rank | THING-TO-RANK |
| ---: | ------------- |
|    1 | JAVA          |
|    2 | NextJS        |
|    3 | Python        |

</details>

<details>
<summary>my test</summary>

| Rank | THING-TO-RANK |
| ---: | ------------- |
|    1 | JAVA          |
|    2 | NextJS        |
|    3 | Python        |

</details>

#### subtitle

### quote

---

> If we pull together and commit ourselves, then we can push through anything.

— Mona the Octocat

### syntax

| style         |    syntax     |                              examples |
| :------------ | :-----------: | ------------------------------------: |
| bold          |   \_\_ \_\_   |                              **bold** |
| italic        |     \_ \_     |                              _italic_ |
| strikethrough |   \~\~ \~\~   |                     ~~strikethrough~~ |
| subscript     | \<sub>\</sub> |   This is a <sub>subscript</sub> text |
| superscript   | \<sup>\</sup> | This is a <sup>superscript</sup> text |
| underline     | \<ins>\</ins> |                  <ins>underline</ins> |

The background color is `rgb(9, 105, 218)` for light mode and `rgb(9, 105, 218)` for dark mode.

### links

[google](www.google.de)

- [Link Text](#collapsed-section)
  - [sub title](#subtitle)
  - my test

### images

![Screenshot of a comment on a GitHub issue showing an image, added in the Markdown, of an Octocat smiling and raising a tentacle.](https://myoctocat.com/assets/images/base-octocat.svg)

### task lists

<input type="checkbox">

### emoji

:mask:
[emoji](https://github.com/ikatyang/emoji-cheat-sheet/blob/github-actions-auto-update/README.md)

### footnotes (only in git)

Here is a simple footnote[^1].

A footnote can also have multiple lines[^2].

[^1]: My reference.
[^2]:
    To add line breaks within a footnote, prefix new lines with 2 spaces.
    This is a second line.

### alerts (only in git)

> [!NOTE]
> Useful information that users should know, even when skimming content.

> [!TIP]
> Helpful advice for doing things better or more easily.

> [!IMPORTANT]
> Key information users need to know to achieve their goal.

> [!WARNING]
> Urgent info that needs immediate user attention to avoid problems.

> [!CAUTION]
> Advises about risks or negative outcomes of certain actions.

### diagrams

#### mermaid

```mermaid
graph TD;
  A-->B;
  A-->C;
  B-->D;
  C-->D;
```

### math

This sentence uses `$` delimiters to show math inline: $\sqrt{3x-1}+(1+x)^2$

$$\left( \sum_{k=1}^n a_k b_k \right)^2 \leq \left( \sum_{k=1}^n a_k^2 \right) \left( \sum_{k=1}^n b_k^2 \right)$$

```math
\left( \sum_{k=1}^n a_k b_k \right)^2 \leq \left( \sum_{k=1}^n a_k^2 \right) \left( \sum_{k=1}^n b_k^2 \right)
```

## everything_about_python

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

  - Level 1: The Foundations

    <input type="checkbox" checked> Solid Python Fundamentals: [official documentation](https://docs.python.org/3/tutorial/index.html) & [classes](https://docs.python.org/3/tutorial/classes.html)

    <input type="checkbox"> First-Class Functions: [Data Model](https://docs.python.org/3/reference/datamodel.html) (master python functions)

    <input type="checkbox"> Closures: A closure is a function that remembers variables from its enclosing scope. [Closure](https://docs.python.org/3/glossary.html#term-closure) & [Naming and Binding](https://docs.python.org/3/reference/executionmodel.html#naming-and-binding)

    - [ ] type introspection (type(), isinstance(), issubclass(), hasattr(), getattr(), and dir())
    - [ ] dynamic attribute access (getattr(), setattr(), delattr())
    - [ ] poetry

  - Level 2: The Building Blocks - Decorators & Descriptors

    <input type='checkbox'> Decorators: [defining functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions) & [function definition](https://docs.python.org/3/reference/compound_stmts.html#function-definitions) & [decorators](https://docs.python.org/3/glossary.html#term-decorator) & [functools](https://docs.python.org/3/library/functools.html) & [call](https://docs.python.org/3/reference/datamodel.html#object.__call__)

    <input type='checkbox'> Descriptors: [descriptor](https://docs.python.org/3/howto/descriptor.html) & [implementing descriptors](https://docs.python.org/3/reference/datamodel.html#implementing-descriptors) & [property()](https://docs.python.org/3/library/functions.html#propert)

  - Level 3: The Deep Magic - Metaclasses

    <input type='checkbox'> [metaclasses](https://docs.python.org/3/reference/datamodel.html#metaclasses)

    <input type='checkbox'> [type()](https://docs.python.org/3/library/functions.html#type)

    <input type='checkbox'> [\_\_new\_\_, \_\_init\_\_, \_\_prepare\_\_](https://docs.python.org/3/reference/datamodel.html#customizing-class-creation)

  - Level 4: Practical Application & The Why

    <input type='checkbox'> [Django ORM](https://docs.djangoproject.com/en/5.2/topics/db/models/) & [SQLAIchemy](https://docs.sqlalchemy.org/en/20/orm/declarative_mapping.html) & [Pydantic](https://docs.pydantic.dev/latest/concepts/models/)

    <input type='checkbox'> [ABCMeta](https://docs.python.org/3/library/abc.html)

  - Level 5: Best Practices & When to Stop

    <input type='checkbox'> [The Zen of Python](https://peps.python.org/pep-0020/)

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
