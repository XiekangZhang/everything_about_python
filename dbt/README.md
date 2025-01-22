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
  - _name_ in snake_case, _version_, _require-dbt-version_, _profile_, _model-paths_, _seed-paths_, _test-paths_, _analysis-paths_, _macro-paths_, _snapshot-paths_, _docs-paths_, _vars_
