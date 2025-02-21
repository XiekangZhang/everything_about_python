# dbt Tutorial

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
- _dbt run --select "stg_customers top_level_emal_domains" --empty_ to build an empty version of the models to save warehouse spend

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

# dbt Fundamentals

- Traditional Data Teams --> Modern Data Teams:
  - Data Analytics & Data Engineer --> Data Analytics & Analytics Engineer (T) & Data Engineer

# dbt Certified Developer Path

## Refactoring SQL for Modularity

- CTE: Common Table Expression

## Jinja, Macros, and Packages

### Jinja Basics

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
