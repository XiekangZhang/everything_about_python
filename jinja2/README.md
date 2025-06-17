# Jinja Documentation

## API

- Jinja uses a central object called the template **Environment** with **PackageLoader**.
- use **get_template()** to read the template file
- the default **Environment** renders templates to strings. With **NativeEnvironment**, rendering a template produces a native Python type.

## Template Designer Documentation

- A Jinja template is simply a text file. Jinja can generate any text-based format. A Jinja template doesn't need to have a specific extension.
- A template contains _variales_ and/or _expressions_, which get replaced with values when a template is _rendered_. _tags_ controls the logic of the template.
- Line Statements and Comments are also possible, though they don't have default prefix characters. To use them, set **line_statement_prefix** and **line_comment_prefix** when creating the **Enviroment**
- basic syntax:

  ```python
    # Variables
    {{ foo.bar }}
    {{ foo['bar'] }}
    # Filters
    {{ listx|join(', ') }} == str.join(', ', listx)
    # Tests by is
    {% if loop.index is divisibleby 3 %}
    # Whitespace Control
    {%+ if something %}yay{% endif %} # disable the lstrip_blocks
    {% if something +%}yay{% endif %} # disable the trim_blocks
    {% for item in seq -%} # remove whitespaces
    # Escaping
    {{ '{{' }}
    {% raw %}...{% endraw %}
    {{ user.username|e }} # manual escaping for HTML
    {{ user.username|safe }} # variables marked as safe will not be escaped
    # converts all operands into strings and concatenates them
    {{ "Hello " ~ name ~ "!" }}
    # inline if
    {{ "[{}]".format(xxx) if xxx else optional }}
    # with block
    {% with a={}, b=a.attribute %}...{% endwith %}
    # autoescape
    {% autoescape true %}...{% endautoescape %}
  ```

- Template Inheritance

  ```python
    {% extends "xxx" %}
    {{ super() }} # to get the result from parent block
    {% extends xxx if xxx is defined else xxb %} # contitional extends
  ```

- Named Block End-Tags

  ```python
    {% block block_name %}{{ variable_outer_of_block }}{% endblock block_name %} # = Empty, by default, a block may not access variables from outside the block
    {% block block_name scoped %}{{ variable_outer_of_block }}{% endblock block_name %}
    {% block block_name scoped required %}{{ variable_outer_of_block }}{% endblock block_name %} # Required blocks may only contain space and comments, and they cannot be rendered directly.
  ```

- List of Control Structures
  - for: `{% for user in users %}...{% endfor %}`, `{% for k, v in my_dict.items() %}`, `{% for k, v in my_dict | dictsort %}`, `{{ loop.cycle('odd', 'even') }}`
    - does not support _break_, or _continue_
    - `{% for user in users recursive %}...{% endfor %}`: iterating over hierarchical data structures by calling itself within the loop
      - usecases:
        - rendering menus
        - displaying file system structures
        - creating nested lists or trees
        - processing any data with a hierarchical or parent-child relationship where the depth is not fixed

### Macros

- macros are comparable with functions in regular programming languages
- if the marco was defined in a different template, you have to import it first. if a macro name starts with an underscore, it's not exported and can't be imported

  - It's important to know that imports are cached and imported templates don't have access to the current template variables, just the globals by default.

    ```python
        {% import 'forms.html' as forms %}
        # or
        {% from 'forms.html' import input as function1, function2%}
    ```

  - you can add _with context_ or _without context_ tag after import. _with context_ means that the imported macros have access to the variables, functions, globals etc. in the current template. _without context_ vice verse.

- in some cases it can be useful to pass a macro to another macro by using _call_. _call_ block works exactly like a macro without a name.

  ```python
    {% macro dump_users(users) -%}
        <ul>
        {%- for user in users %}
            <li><p>{{ user.username|e }}</p>{{ caller(user) }}</li>
        {%- endfor %}
        </ul>
    {%- endmacro %}

    {% call(user) dump_users(list_of_user) %}
        <dl>
            <dt>Realname</dt>
            <dd>{{ user.realname|e }}</dd>
            <dt>Description</dt>
            <dd>{{ user.description }}</dd>
        </dl>
    {% endcall %}
  ```

- you can also use _filters_ directly in macro by warp the code in the special `filter` section: `{% filter upper %} something {% endfilter %}`
- Please keep in mind that it is not possible to set variables inside a block and have them show up outside of it. This also applies to loops. The only exception to that rule are if statements which do not introduce a scope. Otherwise _namespace_ should be used above version of 2.10.
  ```python
    {% set ns = namespace(found=false) %}
    {% for item in items %}
        {% if item.check_something() %}
            {% set ns.found = true %}
        {% endif %}
        * {{ item.title }}
    {% endfor %}
    Found item having something: {{ ns.found }}
  ```
- accessing the parent loop
  ```python
    {% for row in table %}
        <tr>
        {% set rowloop = loop %}
        {% for cell in row %}
            <td id="cell-{{ rowloop.index }}-{{ loop.index }}">{{ cell }}</td>
        {% endfor %}
        </tr>
    {% endfor %}
  ```
- _include_ renders another template and outputs the result into the current template. `{% include ["somthing.jinja"] ignore missing without context %}`

### Builtin Filters

- _groupby_ yields namedtuples of _(grouper, list)_

  ```python
    {% for group in users|groupby('city') %}
        {{ group.grouper }}: {{ group.list|join(", ")}}
    {% endfor %}
  ```

- _reject_ and _rejectattr_ vs _select_ and _selectattr_

  ```python
    {{ numbers|reject('odd') }}
    {{ user|rejectattr("email", "none")}}
    {{ numbers|select("lessthan", 42) }}
    {{ users|selectattr("is_active") }}
  ```

- _unique_

### Builtin Tests

- _divisibleby()_, _eq()_, _even()_, _filter()_, _ge()_, _gt()_, _le()_, _lt()_, _ne()_, _odd()_, _sameas()_
