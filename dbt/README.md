# dbt

- when you install dbt core, you will also need to install the specific **adapter** for your database, connect to dbt core, and set up a **profiles.yml** file.

## dbt projects

- A dbt project informs dbt about the context of your project and how to transform your data.
- dbt projects structure:
  - **dbt_project.yml**: minimum requirement, project configuration file.
  - **models/**: each model lives in a single file and contains logic that either transforms raw data into a dataset that is ready for analytics or, more often, is an intermediate step in such a transformation.
  - **snapshots/**: a way to capture the state of your mutable tables so you can refer to it later.
  - **seeds/**: CSV files with static data that you can load into your data platform with dbt.
  - **data tests/**: SQL queries that you can write to test the models and resources in your project.
  - **macros/**: blocks of code that you can reuse multiple times.
  - **docs/**: Docs for your project that you can build.
  - **sources/**: a way to name and describe the data loaded into your warehouse by your Extract and Load tools.
  - **exposures/**: a way to define and describe a downstream use of your project.
  - **metrics/**: a way for you to define metrics for your project.
  - **groups/**: groups enable collaborative node organization in restricted collections.
  - **analysis/**: a way to organize analytical SQL queries in your project such as the general ledger from your QuickBooks.
  - **semantic models/**: semantic models define the foundational data relationships in MetricFlow and the dbt Semantic Layer, enabling you to query metrics using a semantic graph.
  - **saved queries/**: saved queries organize reusable queries by grouping metrics, dimensions, and filters into nodes visible in the dbt DAG.
- **dbt_project.yml**:
  - _name_ in snake_case
  - _version_
  - _require-dbt-version_
  - _profile_
  - _model-paths_
  - _seed-paths_
  - _test-paths_
  - _analysis-paths_
  - _macro-paths_
  - _snapshot-paths_
  - _docs-paths_
  - _vars_: e.g., _materialized_
- **sources**

  - configure the source once in a _.yml_ file. --> no manuel change about source table in staging any more.
  - lineage marks the source with green.

  ```yml
  # /models/xxx.yml --> sources for raw table
  version: 2
  sources:
    - name: <source_name>
      database: <database_name>
      schema: <schema_name>
      tables:
        - name: <table_name1>
          loaded_at_field: <timestamp_column>
          freshness: # table level freshness
            warn_after: { count: 6, period: hour }
            error_after: { count: 24, period: day }
          filter: <timestamp_column> >= date_sub(current_date(), interval 1 day)
        - name: <table_name2>
          identifier: <private_key_column>
  ```

  ```yml
  # /models/xxx.yml --> sources for test and documentation
  version: 2
  sources:
    - name: <source_name>
      description: <description>
      tables:
        - name: <table_name1>
          description: >
            <description>
          columns:
            - name: <column_name1>
              description: <description>
              tests: # data_tests only supports unique, not_null and accepted_values
                - unique
                - not_null
                - relationships
                - accepted_values
  ```

  - use _dbt source freshness_ to check the freshness of data
  - use _dbt test --select source:\<source_name>_ to run the test on sources

### models

- Models are primarily written as a _select_ statement and saved as a _.sql_ file, which define the transformed data schema.
- Python models are also supported for training or deploying data science models, complex transformations, or where a specific Python package meets a need.
- model pipeline
- Source --> Staging --> Intermediate --> Fact/Dimension

~~#### SQL models~~

#### Python models

- When you run a Python model, the full result of the final **DataFrame** will be saved as a table in your data warehouse.
- _def model(dbt, session) -> DataFrame:_
- _dbt run --select model | folder_name_

### tests

#### data tests

```yml
# /models/xxx.yml --> data test
version: 2
models:
  - name: <source_name>
    description: <description>
      columns:
        - name: <column_name1>
          description: <description>
          data_tests: # now newly named as data_tests
            - unique
            - not_null
            - accepted_values
        - name: <foreign_key>
          tests:
            - relationships:
                to: ref('xxx')|source('xxx')
                field: primary_key


```

- use _dbt test [--select \<model> test_type:generic|singular]_ to run test
- use _dbt test --select source:\*_ to run tests on sources
- single test (under _/tests/xxx.sql_) vs generic test (in _.yml_)

#### unit tests

- when to add a unit test to your model:
- When your SQL contains complex logic:
  - Regex, Data Math, Window functions, case when, Truncation
- When you are writing custom logic to process input data
- Logic for which you had bugs reported before
- Prior to refactoring the transformation logic
- _dbt run --select "stg_customers top_level_email_domains" --empty_ to build an empty version of the models to save warehouse spend

### documentation

- add _description_ in yml files.
- write large documentation separately into a _.md_ file, with macros

```jinja
{% docs doc_name %}
{% enddocs %}
```

and add `description: '{{ doc("doc_name") }}'` back to yml files

- use _dbt docs generate_ to generate documentation

### snapshots

- Analysts often need to look back in time at previous data states in their mutable tables. dbt can snapshot these changes to help you
  understand how values in a row change over time.

| id  | status  | updated_at | dbt_valid_from | dbt_valid_to |
| --- | ------- | ---------- | -------------- | ------------ |
| 1   | pending | 2024-01-01 | 2024-01-01     | 2024-01-02   |
| 1   | shipped | 2024-01-02 | 2024-01-02     | null         |

- Configure your snapshots in YAML files to tell dbt how to detect record changes. _dbt snapshot_

### seeds

- Seeds are CSV files in your dbt project, that dbt can load into your data warehouse using the _dbt seed_ command. Seeds are best suited
  to static data which changes infrequently. _dbt seeds_

### Jinja and macros

```jinja
Expression: {{ ... }}
Statements: {% ... %}
Comments: {# ... #}
```

- jinja

```jinja
{% set payment_methods = ["bank_transfer", "credit_card", "gift_card"] %}
  select
    order_id,
      {% for payment_method in payment_methods %}
      sum(case when payment_method = '{{payment_method}}' then amount end) as {{payment_method}}_amount,
      {% endfor %}
      sum(amount) as total_amount
  from app_data.payments
  group by 1
```

- macros in Jinja are peices of code that can be reused multiple times - they are analogous to "functions" in other programming languages, and are extremely useful if you find yourself repeating code across multiple models.

```jinja
{% macro cents_to_dollars(column_name, sacle=2) %}
  ({{ column_name }} / 100)::numeric(16, {{ scale }})
{% endmacro %}
```

### Metrics

- MetricFlow is a SQL query generation tool designed to streamline metric creation across different data dimensions for diverse business needs.

## dbt tips

- use the _+_ operator on the left of a model _dbt build --select +model_name_ to run a model and all of its upstream dependencies.
- use the _+_ operator on the right of the model \_dbt build --select model_name+ to run a model and everything downstream that depends on it.
- use the _--exclude flag_ to remove a subset of models out of a selection.
- use the _--full-refresh_ flag to rebuild an incremental model from scratch.
- use _seeds_ to create manual lookup tables, like zip codes to states or marketing UTMs to campaigns. _dbt seed_ will build these from CSVs into your warehouse and make them _ref_ able in your models.
- unit tests must be defined in a YML file in your _models/_ directory.
- _dbt compile_ and then _dbt test_

## dbt implementation

- _dbt init <project_name>_
- _dbt build_ vs _dbt run_ and _dbt test_
  - _dbt build_: creates a model and then runs the tests on this model. If the tests fail, no further downstream models are created.
  - _dbt run_ then _dbt test_: test will happen after all models are created.

## dbt Fundamentals

- Traditional Data Teams --> Modern Data Teams:
  - Data Analytics & Data Engineer --> Data Analytics & Analytics Engineer (T) & Data Engineer

## dbt Certified Developer Path

### Refactoring SQL for Modularity

- CTE: Common Table Expression

### Jinja, Macros, and Packages

#### Jinja Basics

- whitespace control `[%-|-%]`

```jinja
{%- set my_cool_string = 'wow! cool' -%}
{{ my_cool_string }}

{% set my_animals = ['lemur', 'wolf', 'panther', 'tardigrade'] %}
{{ my_animals[0] }}

{%- if xxx -%}
{%- else -%}
{% endif %}

{%- set my_dict={key: value} -%}
```

#### Jinja applications

- dynamic setting a variables based on a query

```jinja
{% set results = run_query("SELECT DISTINCT category FROM " ~ ref('products')) %}

{% if execute %}
  {% set categories = results.columns[0].values() %}
{% else %}
  {% set categories = [] %}
{% endif %}

-- Now you can use the 'categories' variable in your SQL
SELECT
  {% for category in categories %}
    SUM(CASE WHEN category = '{{ category }}' THEN sales ELSE 0 END) AS "{{ category }}_sales"{% if not loop.last %},{% endif %}
  {% endfor %}
FROM {{ ref('sales_data') }}
```

#### macros

- Macros are a way of writing functions in Jinja.

```jinja
{% macro <function_name>(parameters...) %}
<code_logic>
{% endmacro %}

{{ function_name(values...) }}
```

#### package

- `dbt deps` to install packages

```yml
pacakges:
  - git:
    revision: <branch_name>
  - package:
    version:
  - local: <local_path>
```

#### Advanced Jinja and Macros

```jinja
{% macro grant_select(schema=target.schema, role=target.role) %}

  {% set sql %}
  grant usage on schema {{ schema }} to role {{ role }};
  grant select on all tables in schema {{ schema }} to role {{ role }};
  grant select on all views in schema {{ schema }} to role {{ role }};
  {% endset %}

  {{ log('Granting select on all tables and views in schema ' ~ target.schema ~ ' to role ' ~ role, info=True) }}
  {% do run_query(sql) %}
  {{ log('Privileges granted', info=True) }}
{% endmacro %}
```

```jinja
{%- macro union_tables_by_prefix(database, schema, prefix) -%}
  {%- set tables = dbt_utils.get_relations_by_prefix(database=database, schema=schema, prefix=prefix) -%}
  {% for table in tables %}
      {%- if not loop.first -%}
      union all
      {%- endif %}
      select * from {{ table.database }}.{{ table.schema }}.{{ table.name }}
  {% endfor -%}
{%- endmacro -%}
```

```jinja
{% macro clean_stale_models(database=target.database, schema=target.schema, days=7, dry_run=True) %}
{% set get_drop_commands_query %}
        select
            case
                when table_type = 'VIEW'
                    then table_type
                else
                    'TABLE'
            end as drop_type,
            'DROP ' || drop_type || ' {{ database | upper }}.' || table_schema || '.' || table_name || ';'
        from {{ database }}.information_schema.tables
        where table_schema = upper('{{ schema }}')
        and last_altered <= current_date - {{ days }}
{% endset %}

{{ log('\nGenerating cleanup queries...\n', info=True) }}
{% set drop_queries = run_query(get_drop_commands_query).columns[1].values() %}
{% for query in drop_queries %}
  {% if dry_run %}
    {{ log(query, info=True) }}
  {% else %}
    {{ log('Dropping object with command: ' ~ query, info=True) }}
    {% do run_query(query) %}
    {% endif %}
{% endfor %}
{% endmacro %}
```

### Advanced Materializations

- Materialization handles how to build your model
  - ephemeral: the `final/model` table will not be created. It used as a `CTE`
  - views: saved query. Starting with _views_
  - tables: if the view query lasts too long, change to _tables_
  - incremental: keep the old table, and add the new records, working with `unique_key='<id>'` to ~~activate `merge` query~~. If dbt builds lasts too long, switch to _incremental_
    - `is_incremental()` checks 4 conditions --> only true, true, true, false
      1. Does this model already exist as an object in the database
      2. Is that database object a table?
      3. Is this model configured with `materialized='incremental'`?
      4. Was the `--full-refresh` flag passed to this `dbt run`?
    - incremental materialization limitations --> ignorance grade e.g., cutoff vs late arrvials (weekly `--full-refresh`)
    - What about truly massive datasets?
      - always rebuild past 3 days. Fully ignore late arrvials
      - always replace data at the partition level
      - no unique keys - `merge` is expensive than `insert` (usually: `update` + `insert` > `delete` + `insert`)
    - Should I use an incremental model?
      - Good candidates
        - Immutable event streams: tall + skinny table, append-only, no updates
        - if there are any updates, a reliable _updated_at_ field
      - Not-so-good candidates
        - you have small-ish data
        - your data changes constantly: new columns, renamed columns, etc.
        - your data is updated in unpredictable ways
        - your transformation performs comparions or calculations that require other rows
    - To sum up: Most incremental models are **approximately correct**, windows function has to be defined. Prioritizing correctness can negate performance gains from incrementality
  - snapshots: underlying table + which rows are changed. --> changed data will be added into new rows. Using `dbt snapshot`
    ```jinja
    {% snapshot mock_orders %}
    {% set new_schema = target.schema + '_snapshot' %}
    {{ config(target_database='analytics',
              target_schema=new_schema,
              unique_key='order_id',
              strategy='timestamp',
              updated_at='updated_at')
    }}
    select * from analytics.{{target.schema}}.mock_orders
    {% endsnapshot %}
    ```

### Analyses and Seeds

#### Analyses

- it is used to test your queries before modifying database
- sql files in the analyses folder, no models and no tests
- support jinja
- can be compiled with `dbt compile`

#### Seeds

- csv files in the data folder
- build a table from a small amount of data in a csv files by using `dbt seed`
- _models_ can _ref_ seed
- using `dbt seed --models <model_name>` to run seed including test --> needing _.yml_

### Exposures

- fully document your data ecosystem
- you can use `dbt run --select +exposure:*`

```yml
exposures:
  - name: orders_data
    label: orders_data
    type: notebook
    maturity: high
    url: https://tinyurl.com/jaffle-shop-reporting
    description: "Exposure for orders data"
    depends_on:
      - ref('fct_orders')
      - metric(xxx)
    owner:
      name: Michael McData
      email: data@jaffleshop.com
```

- _exposures_ are always used with _metrics_.

```yml
semantic_models: ...
metrics: ...
```

- running metric to see a result: `dbt sl query --metrics xxx`

### Understanding state

- `dbt run --select state:modified+`
- `dbt retry` starting building models further where it failed last time

### dbt Mesh

- Monolithic data strucutre vs dbt Mesh
- dbt Mesh: decentralized data --> to give the right people the right permission and the right report, like different departments

#### Model Governance

##### Model Contracts

- allow you to guarantee the shape of your model
  - columns & names
  - data type of each column
  - materialized type
- adding `contract: enforced: true` flag into your model _.yml_ file

##### Model versions

- rename model name to _model_v2.sql_
- `ref('model', v=2)` `dbt run -s xxx version:latest`

```yml
models:
  - name: xxxx
    latest_version: 2
    versions:
      - v: 1
        config:
          alias: xxxxxx
      - v: 2
        columns:
          - include: xxx
            exclude: xxx
          - name: xxx
            data_type: xxx
```

##### Groups and Access Modifiers

- help to navigate to your needing models. Useful for large project

```yml
groups:
  - name: finance
    owner:
      name: Firstname Lastname
      email: finance@jaffleshop.com
      slack: finance-data
      github: finance-data-team
  - name: product
    owner:
      email: product@jaffleshop.com
      github: product-data-team
```

- access modifiers: _public, protected, private_

```yml
groups:
  - name: fct_orders
    group: finance
    access: public
```

#### Multi-Project Collaboration

- better for collaborate

##### Cross-Project Ref

- set up `dependencies.yml` then `{{ ref('<project_name>', '<model_name>') }}`

```yml
projects:
  - name: core_platform
```

##### Cross-Project Orchestration

- run downstream project after upstream project runnning

### Advanced Testing

- interactive / ad hoc queries

```sql
select custom_id
from customers
group by customer_id
having count(*) > 1
```

- standalone saved query

#### Test coverage

- `dbt run-operation <required_tests>`
- _dbt_meta_testing_ package
- _freshness test_ only working on source
- you can adding `{{ config(required_tests=None) }}` to exclude the specific models out of tests

#### Test Deployment & Commands

- `dbt test --select model1 model2` to run test on both models
- `dbt test --select model1,model2` to run test on interaction of models
- `dbt test --select test_type=singluar|generic`
- `dbt test --exclude model1`
- `dbt test --store-failures`
- best way: `dbt build --fail-fast`

#### Custom Tests

- singular test in sql
- generic singular test using `{% test <function_name(parameters)> %}...{% endtest %}` marcos and migrate the test into _yml_ file

#### Tests in Packages

```jinja
{#
-- use this set if you are comparing to a legacy model, rather than another dbt model
-- {% set old_etl_relation=adapter.get_relation(
--       database=target.database,
--       schema="old_etl_schema",
--       identifier="fct_orders"
-- ) -%}
#}

-- use this set if you are comparing to another dbt model
{% set old_etl_relation=ref('orders__deprecated') %}

-- this is your newly built dbt model
{% set dbt_relation=ref('orders') %}

{{ audit_helper.compare_relations(
    a_relation=old_etl_relation,
    b_relation=dbt_relation,
    primary_key="order_id"
) }}
```

#### Test Configurations

```yml
models:
  - name: customers
    description: One record per customer
    columns:
      - name: customer_id
        description: Primary Key
        data_tests:
          - unique:
            config:
              where: "order_date > '2018-03-01'" # like sql
              limit: 10 # like sql
              store_failures: true|false #
              schema: test_failures # specified which schema should be used to store the failures --> change the suffix
          - not_null:
            config:
              severity: warn|error #
              error_if: ">100" #
              warn_if: ">50" #
```

### Advanced Deployment

- direct promotion vs indirect promotion (QA Branch) --> only run on custom branch
- adding `tags` to minimize building models

#### Common deployment jobs

- standard job with `dbt build`
- full refresh job with `dbt build --full-refresh`: rebuild incremental models and seeds
- time sensitive
- fresh rebuild

#### CI

- best practices `dbt run -s state:modified+` + `dbt test -s state:modified+` + _defer_ (compare state)
- by activating webhooks --> trigger after pull request

#### custom environment behavior & environment variables

- you can use `target.schema` and `target.name` to custom environment behavior
- `{{ env_var('DBT_MY_ENV', '<default_value>') }}` to get environment variable

## Other tipps

- `describe table {{ source(......)}}` to have an overview of the table
- `dbt_utils`, `dbt_expectations`, `audit_helper` are necessary packages for every dbt project
- overwriting tests by using the same name
- What might happen if two overlapping jobs attempt to run the same database model at the same time? --> Only the first job will complete, and the second will remain queued
- `{% do exceptions.warn(...) %}` and `{{ exceptions.raise_compiler_error(...)}}`
- `{% if execute %}`
- `target.name`
- `dbt --record-timing-info | -r xxx.txt run` --> `snakeviz xxx.txt`

### Cron

- minute hour day(month) month day(week) --> `*/30 6-23 * * 1-5` --> every 30 minutes, for hours between 6am and 11pm UTC, from Monday to Friday
- `15,45 0-4,8-23 * * 0` every 15 and 45 of hour between 0-4 and 8-23 on Sunday

### Change Data Capture (CDC) vs Slowly Changing Dimensions (SCD)

- CDC - it's about the how of detecting changes
  - to efficiently replicate changes from source systems to target systems in near real-time
  - to minimize the impact on source systems by only transferring changed data
- SCD - it's about the how of storing historical data
  - to maintain a historical record of changes in dimension tables, allowing for accurate historical analysis
  - to provide context for historical data by preserving past versions of dimension records
  - Types:
    - SCD Type 1: overwrites existing data
    - SCD Type 2: creates a new row for each change
    - SCD Type 3: adds a new column to store previous values

### dbt Clone

- copy a data object without underlying data
  - requirements
    - job run successfully on _prod_ environment
    - _defer_ is activated in _prod_
    - `dbt clone`

### grants

- you can configure _grants_ for example in _dbt_project.yml_ to apply grants

```yml
seeds:
  - name: seed_name
    config:
      grants:
        select: []
```

### python models

- perform analysis using tools from opne-source python ecosystem

```py
def model(dbt, session):
  ...
  return final_df
```

### jinja

- Filters `{{ name | striptags | title }}`

#### Jinja Data Structures & Methods Overview

Jinja offers a few core data structures for templating:

**1. Lists (Arrays)**

- **Creation:** `[1, 2, "a"]`, `[]`
- **Methods/Filters:**
  - `| length`: Get list length.
  - `| first`: Get first element.
  - `| last`: Get last element.
  - `| join(sep)`: Join elements with separator.
  - `| sort`: Sort list.
  - `| reverse`: Reverse list.
  - `| map(attr)`: Apply function to elements.
  - `| select(attr)`: Filter list.
  - `append(value)`: add item to the end (using `{% do %}`)
- **Access:** `list[index]`

**2. Dictionaries (Maps)**

- **Creation:** `{"key": "value", "num": 123}`, `{}`
- **Methods:**
  - `.items()`: Get key-value pairs.
  - `.keys()`: Get keys.
  - `.values()`: Get values.
  - `.update(dict)`: Merge/update (using `{% do %}`).
- **Access:** `dict["key"]`, `dict.key`

**3. Strings**

- **Creation:** `"Hello"`, `'World'`
- **Methods/Filters:**
  - `| length`: Get string length.
  - `| upper`: Convert to uppercase.
  - `| lower`: Convert to lowercase.
  - `| replace(old, new)`: Replace substrings.
  - `| trim`: Remove whitespace.
  - `| title`: Capitalize words.
  - `| split(sep)`: Split string.
  - string slicing: `string[start:end]`
- **Concatenation:** `string1 ~ string2`

**4. Numbers (Integers, Floats)**

- **Arithmetic:** `+`, `-`, `*`, `/`, `//`, `%`, `**`
- **Filters:**
  - `| round(precision)`: Round number.
- **Comparisons:** `==`, `!=`, `>`, `<`, `>=`, `<=`

**Key Notes:**

- Jinja is primarily for templating, not complex logic.
- `{% do %}` is needed for in-place modifications (e.g., `append()`, `update()`).
- Filters (`|`) transform data.
- Jinja is not python, and does not have classes like python does.

### Node selection syntax

| command       | argument(s)                                               |
| ------------- | --------------------------------------------------------- |
| run           | --select, --exclude, --selector, --defer                  |
| test          | --select, --exclude, --selector, --defer                  |
| seed          | --select, --exclude, --selector                           |
| ls            | --select, --exclude, --selector, --resource-type          |
| compile       | --select, --exclude, --selector, --inline                 |
| freshness     | --select, --exclude, --selector                           |
| build         | --select, --exclude, --selector, --resource-type, --defer |
| docs generate | --select, --exclude, --selector                           |

- `--exclude` exclude models from your run
- `--defer` makes it possible to run a subset of models or tests in a sandbox environment without having to first build their upstream parents. It is usually used with `--state` together. `dbt test --select 'model_b' --defer --state <prod-run-artifacts>`
- Node selector methods

| wildcard | description                                               |
| -------- | --------------------------------------------------------- |
| \*       | matches any number of any characters (including none)     |
| ?        | matches any single character                              |
| [abc]    | matches one character given in the bracket                |
| [a-z]    | matches one character from the range given in the bracket |

- operators

```sh
dbt run --select "+my_model+|+my_model|my_model+"
dbt run --select "3+my_model+4"

# the @ operator is similar to +, but will also include all ancestors of all descendants of the selected model
dbt run --select "@my_model"

# unions
dbt run --select "+snowplow_sessions +fct_orders"

# intersections
dbt run --select "stg_invoices+,stg_accounts+,tag:nightly"

dbt list --select "*.folder_name.*"
dbt list --select "access:public|config.materialized:incremental|group:finance|+metric:weekly_active_users|source:snowplow+|semantic_model:*|fqn:some_model" # fully qualified names (FQN) is composed of the project name, suddirectories with the path, and the file name without extension separated by periods
dbt run --select "result:error|fail" --state path/to/artifacts

dbt run --select "state:modified|old|unmodified"

dbt test --select "test_name:unique"
dbt test --select "test_type:unit|data|generic|singular"
dbt test --select "unit_test:*"

dbt list --select "version:latest"

```

- _selector_ simplifies running complex commands

```sh
# without selectors
dbt run --select @source:snowplow,tag:nightly models/export --exclude package:snowplow,config.materialized:incremental export_performance_timing
```

```yml
# with selectors
selectors:
  - name: nightly_diet_snowplow
    description: "Non-incremental Snowplow models that power nightly exports"
    definition:
      union:
        - intersection:
            - "@source:snowplow"
            - "tag:nightly"
        - "models/export"
        - exclude:
            - intersection:
                - "package:snowplow"
                - "config.materialized:incremental"
            - export_performance_timing
```

```sh
# then
dbt run --selector nightly_diet_snowplow
```

### dbt_project.yml

- dbt demarcates between a folder name and a configuration by using a `+` prefix before the configuration name. --> use the `+` prefix to help clarify the difference between resource paths and configs in _dbt_project.yml_ files.

### DAG Auditing & how we structure our dbt projects

#### DAG Auditing

- are there any direct joins from sources into an intermediate model? (staging model is needed for each source to be cleaned and standardized)
- do sources join directly together? (staging model is needed)
- are there any rejoining of upstream concepts?
- are models in the same layer dependent on each other?
- dbt project needs a defined end point
- is there repeated logic found in multiple models?

#### How we structure our dbt projects

- staging: creating our atoms, our initial modular building blocks, from source data
  - subdirectories based on the source system
  - file name: _stg\_[source]\_\_[entitys].sql_
  - the most standard types of staging model transformations are:
    - Renaming
    - Type casting
    - Basic computations e.g., cents to dollars
    - categorizing e.g., `case when`
  - materialized as views
  - staging models are the only place we'll use the `source` macro, and our staging models should have a 1-to-1 relationship to our source tables.
- intermediate: stacking layers of logic with clear and specific purposes to prepare our staging models to join into the entities we want
  - subdirectories based on business groupings
  - file name: _int\_[source]\_\_[entity]s\_[verb]s.sql_
  - materialized ephemerally | materialized as views in a custom schema with special permissions
- marts: brigning together our modular pieces into a wide, rich vison of the entities our organization cares about
  - group by department or area of concern
  - name by entity
  - materialized as tables or incremental models
  - wide and denormalized (modern way)

### Exposures

- available properties
  - required: **name**, **type: dashboard|notebook|analysis|ml|application**, **owner: name & email**
  - expected: **depends_on: - ref(...) | - source(...) | - metric(...)**
  - optional: **label**, **url**, **maturity**, **description**, **tags**, **meta**

### env_var function

- you can use `{{ env_var('variable_name', 'default_value') }}` in all _.yml_ file

### grants

```yml
models:
  +grants:
    select: ["user_a", "user_b"]

# add new grantees
{{ config(grants = {'+select': ['user_c']} }}

# conditional grants
models:
  +grants:
    select: "{{ ['user_a', 'user_b'] if target.name == 'prod' else ['user_c'] }}"

# BigQuery examples
{{ config(grants={'roles/bigquery.dataViewer': ['user:someone@yourcompany.com']} }}

models:
  - name: specific_model
    config:
      grants:
        roles/bigquery.dataViewer: ['user:someone@yourcompany.com']
```

### model governance

#### model access

- make models with right access modificator, e.g., _public_, _private_ (same group), _protected_ (same project)
- _access_ level should be used with _group_ together
- it is recommended to set the access modifier of a new model to _private_ to prevent other project resources from taking dependencies on models not intentionally designed for sharin across groups

#### model contracts

- supported
  - SQL models
  - _table_, _view_, _incremental_ with _on_schema_change: append_new_columns | fail_
- when enforced, your contract must include every column's _name_ and _data_type_

#### model versions

- model version could be used with _deprecation_date_ together
- you need but create a new model `<old_data_model>_v<version>.sql`
- in _.yml_ file you only need to write down the differences between the previous version and actual version
  ```yml
  models:
    - name: dim_customers
      latest_version: 1
      config:
        materialized: table
        contract: { enforced: true }
      columns:
        - name: customer_id
          description: this is the primary key
          data_type: int
        - name: country_name
          description: where this customer lives
          data_type: varchar
      versions:
        - v: 1 # matches what's above -- nothing more meeded
          config:
            alias: dim_customers
        - v: 2
          columns:
            - include: all
              exclude: [country_name] # mark only the diff
  ```
- `{{ ref('my_dbt_project', 'my_model', v='3') }}` to use different version in ref jinja

```bash
dbt run --select dim_customers.v2 | dim_customers_v2
dbt run -s dim_customers,version:latest
```

#### project dependencies

- the _dependencies.yml_ file can contain both types of dependencies: "package" and "project" dependencies
- Project dependencies vs. Package dependencies
  - project dependencies are designed for the dbt Mesh and cross-project reference workflow. But private packages and jinja are not supported in _dependencies.yml_.
  - package dependencies allow you to add source code from someone else's dbt project into your own, like a library. Use _packages.yml_ to include packages, including private packages and supporting jinja.

### deployment and testing

- PR template from dbt labs
  - description & motivation
  - to-do before merge
  - screenshots
  - validation of models
  - changes of existing models
  - checklist

### Hooks and operations

- Hooks are snippets of SQL that are executed at different times:
  - `pre-hook`: executed _before_ a model, seed or snapshot is built
  - `post-hook`: executed _after_ ad model, seed or snapshot is built
  - `on-run-start`: executed at the _start_ of `dbt build`, `dbt compile`, `dbt docs generate`, `dbt run`, `dbt seed`, `dbt snapshot`,
    or `dbt test`
  - `on-run-end`: executed at the _end_ of other commands
  ```sql
  {{ config(pre_hook=["{{ some_macro() }}" | <sql_statements>]) }}
  ```
  ```bash
  dbt run-operation {marco_name} --args '{role: reporter}'
  ```

### Custom schemas

| target schema | custom schema | resulting schema    |
| ------------- | ------------- | ------------------- |
| alice_dev     | none          | alice_dev           |
| alice_dev     | marketing     | alice_dev_marketing |

- if your dbt project has a custom macro called _generate_schema_name_, dbt will use it instead of the default macro.
- A built-in alternative pattern for generating schema names

  - `target.name == 'prod'`

    | target schema  | custom schema | resulting schema |
    | -------------- | ------------- | ---------------- |
    | analytics_prod | none          | analytics_prod   |
    | analytics_prod | marketing     | marketing        |

  - `target.name != 'prod'`

    | target schema | custom schema | resulting schema |
    | ------------- | ------------- | ---------------- |
    | alice_dev     | none          | alice_dev        |
    | alice_dev     | marketing     | alice_dev        |

  if you want to use this pattern, please create a macro under _/macros/_ named as _generate_schema_name.sql_ with following jinja

  ```jinja
  {% macro generate_schema_name(custom_schema_name, node) -%}
    {{ generate_schema_name_for_env(custom_schema_name, node) }}
  {%- endmacro %}
  ```

### Project variables

- to use a variable in a model, hook, or macro, use the {{ var('...') }} function
- variables can be defined in two ways:
  - in the _dbt_project.yml_ file
    ```yml
    name: my_dbt_project
    version: 1.0.0
    config-version: 2
    vars:
      start_date: "2016-06-01"
      my_dbt_project:
        platforms: ["web", "mobile"]
      snowplow:
        app_ids: ["marketing", "app", "landing-page"]
    ```
  - on the command line
    ```bash
    dbt run --vars '{key: value, date: 20180101}'
    ```

## Reference

### Project configs

- dbt_project.yml
  - `--project-dir` flag or the `DBT_PROJECT_DIR` to change the default directory for _dbt_project.yml_.
  - use **relative path**
  - `analysis-paths: ["relative_path"]`
  - `asset-paths: ["relative_path"]`: will be compiled as part of `docs generate`
  - `clean-targets: ["relative_path", "relative_path", ...]`
  - `config-version: 2`
  - `dispatch` search the namespace in the given order
  ```yml
  dispatch:
    - macro_namespace: dbt_utils
      search_order: ["my_root_project", "dbt_utils"]
  ```
  - `docs-paths: ["relative_path"]`
  - `macro-paths: ["relative_path"]`
  - `name: project_name`: snake_case
  - `on-run-start` and `on-run-end`
  - `packages-install-path: relative_path`
  - `profile: string`: the profile your dbt project should use to connect to your data warehouse
  - `query-comment`
  ```yml
  query-comment:
    comment: string
    append: true | false
    job-label: true | false # BigQuery only
  ```
  - `quoting`
  ```yml
  quoting:
    database: true | false
    schema: true | false
    identifier: true | false
  ```
  - `require-dbt-version: ">=1.0.0,<2.0.0"`: but you can disable version checks - `dbt run --no-version-check`
  - `snapshot-paths: ["relative_path"]`
  - `seed-paths: ["relative_path"]`
  - `model-paths: ["relative_path"]`
  - `test-paths: ["relative_path"]`
  - `version: version`: dbt project version vs. `version: 2` in property file refers to dbt version
- .dbtignore

### Resource configs and properties

```yml
# apply config to all models
models:
  +enabled: false
# apply config to all models in your project
name: jaffle_shop
models:
  jaffle_shop:
    +enabled: false
# apply config to all models in a subdirectory
name: jaffle_shop
models:
  jaffle_shop:
    staging:
      +enabled: false
# apply config to a specific model
name: jaffle_shop
models:
  jaffle_shop:
    staging:
      stripe:
        payments:
          +enabled: false
```

#### Configs and properties

- properties describe resources, while configurations control how dbt builds them in the warehouse
- config priority order: in-file `config()` --> properties in a `.yml` file --> config defined in the project file

#### General properties

- **columns** supports `name, data_type, tags, meta, tests, description, quote`
- **constraints** only `table, incremental` models support constraints and constrains require the declaration and enforcement of a model `config: contract: {enforced: true}`
  - `type: not_null|unique|primary_key|foreign_key|check|custom`
  - `expression`
  - `columns` (model-level only)
  - `to` and `to_columns` for **foreign key**
- **deprecation_date** supports RFC 3339 formats include: `YYYY-MM-DD hh:mm:ss.sss±hh:mm`, `YYYY-MM-DD hh:mm:ss.sss` and `YYYY-MM-DD`
- **description**
- **latest_version | version**
  ```yml
  version: 2
  models:
    - name: <model_name>
      latest_version: 2
      versions:
        - v: 3 # required --> numeric or any string
          defined_in: <file_name> # default <model_name>_v<v>
          columns:
            - include: <include_value>
              exclude: <exclude_list>
            - name: <column_name> # additional columns
        - v: 2
        - v: 1
  ```
- **data_tests | tests**: `not_null, unique, accepted_values, relationships`
- **docs**
  ```yml
  # basic
  models:
    - name: my_model
      docs:
        show: true | false
        node_color: purple
  # mark a model as hidden
  models:
    - name: sessions__tmp
      docs:
        show: false
  ```

#### General cofigs: sources, exposures do not support config --> the following configs can be used in top-level

- `access: private | protected (default) | public`: private: same group, protected: same project/package, public: any
- `alias: <user_firendly_name>`
- `contracts: enforced: true`: only for SQL models (22.05.2025), supports _view_, _table_, _incremental_ with _on_schema_change: append_new_columns | fail_
  - if you use contracts and data type, _numeric(38,3)_ should be defined with precision and scale
- `database: <database_name|project_name>`: save the result into the defined database not in default target database = project within BigQuery
- `enabled: true | false`: for enabling or disabling a resource
- `event_time: my_time_field`: is required for the _incremental microbatch_ strategy to understand when an event occurred
  - for incremental microbatch models, if your upstream models don't have _event_time_ configured, dbt cannot automatically filter them during batch processing and will perform full table scans on every batch run
  - the timestamp of the event should represent "at what time did the row occur" rather than an event ingestion date
  - `loaded_at`, `ingested_at` or `last_updated_at` could be used but should take care about duplicates
- `grants: <(+)privilege>: <grantees|principles>`: `+` add a new grantee to the exsiting privilege
  - if you delete the entire `+grants` section, dbt assumes you no longer want it to manage grants and doesn't change anything. To have dbt revoke all existing grants from a node, provide an **empty list** of grantees
  - `grant_access_to`: enables you to set up authorized views. When configured, dbt provides an authorized view access to show partial information from other datasets, without providing end users with full access to those underlying datasets
  ```yml
  models:
    - name: specific_model
      config:
        grant_access_to:
          - project: project_1
            dataset: dataset_1
        grants:
          roles/bigquery.dataViewer: ["user:someone@yourcompany.com"]
  ```
- `group: <group_name>`: assign a group to a resource. When a resource is grouped, dbt will allow it to reference private models within the same group
- `meta: {<dictionary>}`: this metadata is compiled into the `manifest.json` file generated by dbt, and is viewable in the auto-generated documentation
- `persist_docs: relation: true|false columns: true|false`: allow save relation and columns description
- `pre-hook|pre_hook, post-hook|post_hook`: use `.render()` method to avoid compilation errors and to explicitly tell dbt to process a specific relation, when using the `--empty` flag
  ```jinja
  {{ config(pre_hook=["alter external table {{ source('sys', 'customers').render() }} refresh"]) }}
  ```
  - hooks are cumulative
    - hooks from dependent packages will be run before hooks in the active package
    - hooks defined within the model itself will be run after hooks defined in _dbt_project.yml_
    - hooks within a given context will be run in the order in which they are defined
  - run these hooks outside of transaction by using `before_begin` and `after_commit` or set `transaction: False|false`
- `schema: <schema_name>`: the relation is then `{{target.schema}}_{{schema_name}}`
- `tags: [<string>]`
- `unique_key=[<column_name>]`: only in incremental and snapshots
- `full_refresh`: allows you to optionally configure whether a resource will always or never perform a full-refresh

#### for models

- `on_configuration_change: apply | continue | fail`
- `sql_header` vs `pre-hooks`

#### for seeds

- `quote_columns: true|false`
- `column_types: {column_name: datatype}`: column_name is case-sensitive
- `delimiter: <string>`

#### for snapshots

- since dbt core 1.9, define snapshots in a _.sql_ file using a config block is a legacy method.

```yml
snapshots:
  - name: orders_snapshot
    relation: source{} | ref{}
    config:
      strategy: timestamp | check
      updated_at: updated_at # required if you use timestamp strategy
      check_cols: ["col1", "col2"] # required if you use check strategy
      unique_key: id
      pre_hook: <sql_query>
      post_hook: <sql_query>
      dbt_valid_to_current: "to_date('9999-12-31')"
      hard_deletes: "ignore | invalidate | new_record"
      snapshot_meta_column_names:
        dbt_valid_from: strat_date
        dbt_valid_to: end_date
        dbt_scd_id: string
        dbt_updated_at: string
        dbt_is_deleted: string
```

#### for data tests

- singular test
  ```sql
  -- tests/<filename>.sql
  {{config(store_failures=true)}}
  ```
- generic test block
  ```sql
  -- macros/<filename>.sql --> in .yml
  {% test <testname>(model, column_name) %}
  {{ config(store_failures = false) }}
  select ...
  {% endtest %}
  ```

```yml
version: 2
models:
  - name: my_model
    columns:
      - name: my_columns
        tests:
          - unique:
              config:
                fail_calc: "case when count(*) > 0 then sum(n_records) else 0 end"
                severity: error # error --> check error_if then warn_if, warn --> only warn_if
                error_if: ">1000"
                warn_if: ">10"
          - accepted_values:
              values: ["a", "b", "c"]
              config:
                limit: 1000 # will only include the first 1000 failures --> good idea working with large dataset
                store_failures: true|false
                store_failures_as: ephemeral|table|view
                where: "date_column > __3_days_ago__"
```

```sql
-- macros/custom_get_where_subquery.sql --> to create custom where configuration
{% macro get_where_subquery(relation) -%}
    {% set where = config.get('where') %}
    {% if where %}
        {% if "_days_ago__" in where %}
            -- {# replace placeholder string with result of custom macro #}
            {% set where = replace_days_ago(where) %}
        {% endif %}
        {%- set filtered -%}
            (select * from {{ relation }} where {{ where }}) dbt_subquery
        {%- endset -%}
        {% do return(filtered) %}
    {%- else -%}
        {% do return(relation) %}
    {%- endif -%}
{%- endmacro %}

{% macro replace_days_ago(where_string) %}
    {# Use regex to search the pattern for the number days #}
    {# Default to 3 days when no number found #}
    {% set re = modules.re %}
    {% set days = 3 %}
    {% set pattern = '__(\d+)_days_ago__' %}
    {% set match = re.search(pattern, where_string) %}
    {% if match %}
        {% set days = match.group(1) | int %}
    {% endif %}
    {% set n_days_ago = dbt.dateadd('day', -days, current_timestamp()) %}
    {% set result = re.sub(pattern, n_days_ago, where_string) %}
    {{ return(result) }}
{% endmacro %}
```

#### for unit tests

- unite tests validate your SQL modeling logic on a small set of static inputs before you materialize your full model in production. They support a test-driven development approach, improving both the efficiency of developers and reliability of code.
- to run only your unit tests, use the command: `dbt test --select test_type:unit`
- unit tests must be defined in a YML file in your _models/_ directory
- if you want to unit test a model that depends on an ephemeral model, you must use `format: sql` for that input
  ```yml
  unit_tests:
    - name: test_is_valid_email_address
      model: dim_customers
      versions:
        include:
          - 2
        exclude:
          - 1
      overrides:
        is_incremental: false # unit test this model in "full refresh" mode
        dbt_utils.star: col_a, col_b, col_c
      given:
        - input: ref('stg_customers')
          fromat: dict # default --> sql | csv
          rows:
            - { email: bbb@test.com, email_top_level_domain: test.com }
        - input: ref('top_level_email_domains')
          format: sql
          rows: |
            select 'test.com' as tld union all
            select 'gmail.com' as tld
      expect:
        format: sql
        fixture: valid_email_address_fixture_output # tests/fixtures
        # or
        rows:
          - { email: bbb@test.com, is_valid_email_address: true }
          - { email: bbb@xxx.com, is_valid_email_address: false }
  ```

#### for sources

- disable all sources imported from a package
  ```yml
  # dbt_project.yml
  sources:
    events:
      +enabled: false
  ```
- conditionally enable a single source
  ```yml
  # sources.yml
  version: 2
  sources:
    - name: my_source
      config:
        freshness:
          warn_after:
            count: <positive_integer>
            period: minute | hour | day
          error_after:
            count: <positive_integer>
            period: minute | hour | day
          filter: datediff('day', _etl_loaded_at, current_timestamp) < 2
      loaded_at_field: <column_name_or_expression> # completed_date::timestamp | CAST(completed_date AS TIMESTAMP)
      loaded_at_query: <sql_expression> # not be used if loaded_at_field is defined
      tables:
        - name: my_source_table
          identifier: <table_identifier> # the table name as stored in the database. By default, dbt will use the table's name parameter as the identifier
          config:
            event_time: my_time_field
            enabled: "{{ var('my_source_table_enabled', false) }}"
        - name: <table_name>
          external:
            location: <string>
            file_format: <string>
            row_format: <string>
            tbl_properties: <string>
            partitions:
              - name: <column_name>
                data_type: <string>
                description: <string>
                config:
                  meta: { dictionary }
  ```

## advanced topics

### create new materializations

[custom materializations](https://github.com/dbt-labs/dbt-adapters/tree/60005a0a2bd33b61cb65a591bc1604b1b3fd25d5/dbt/include/global_project/macros/materializations)

```jinja
{% materialization my_materialization_name, default %}
 -- cross-adapter materialization... assume Redshift is not supported
{% endmaterialization %}


{% materialization my_materialization_name, adapter='redshift' %}
-- override the materialization for Redshift
{% endmaterialization %}
```

- anatomy of a materialization
  - prepare the database for the new model
  - run pre-hooks
  - execute any sql required to implement the desired materialization
  - run post-model hooks
  - clean up the database as required
  - update the relation cache

### create user-defined functions

### define and use custom snapshot strategy

- `snapshot_<strategy>_strategy`
