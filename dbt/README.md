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
  - _vars_

### models

- Models are primarily written as a _select_ statement and saved as a _.sql_ file.
- Python models are also supported for training or deploying data science models, complex transformations, or where a specific Python package meets a need.

#### SQL models

#### Python models

- When you run a Python model, the full result of the final **DataFrame** will be saved as a table in your data warehouse.
- _def model(dbt, session) -> DataFrame:_
- _dbt run --select model_

### tests

#### data tests

#### unit tests

- when to add a unit test to your model:
  - When your SQL contains complex logic:
    - Regex, Data Math, Window functions, case when, Truncation
  - When you are writing custom logic to process input data
  - Logic for which you had bugs reported before
  - Prior to refactoring the transformation logic
- _dbt run --select "stg_customers top_level_emal_domains" --empty_ to build an empty version of the models to save warehouse spend

### documentation

- documentation have to be written and stored in _.md_ extension.

### snapshots

- Analysts often need to look back in time at previous data states in their mutable tables. dbt can snapshot these changes to help you
  understand how values in a row change over time.

| id  | status  | updated_at | dbt_valid_from | dbt_valid_to |
| --- | ------- | ---------- | -------------- | ------------ |
| 1   | pending | 2024-01-01 | 2024-01-01     | 2024-01-02   |
| 1   | shipped | 2024-01-02 | 2024-01-02     | null         |
- Configure your snapshots in YAML files to tell dbt how to detect record changes. _dbt snapshot_

### seeds

## dbt tips

- use the _+_ operator on the left of a model _dbt build --select +model_name_ to run a model and all of its upstream dependencies.
- use the _+_ operator on the right of the model \_dbt build --select model_name+ to run a model and everything downstream that depends on it.
- use the _--exclude flag_ to remove a subset of models out of a selection.
- use the _--full-refresh_ flag to rebuild an incremental model from scratch.
- use _seeds_ to create manual lookup tables, like zip codes to states or marketing UTMs to campaigns. _dbt seed_ will build these from CSVs into your warehouse and make them _ref_ able in your models.
- unit tests must be defined in a YML file in your _models/_ directory.
