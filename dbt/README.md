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
              data_tests: # now newly named as data_tests
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
- Source --> Staging --> Intermediate --> Fact --> Dimension

#### SQL models

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
  - incremental: keep the old table, and add the new records, working with `unique_key='<id>'` to activate `merge` query. If dbt builds lasts too long, switch to _incremental_
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

## Other tipps

- `describe table {{ source(......)}}` to have an overview of the table

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
