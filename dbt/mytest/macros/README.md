## macro create_model_yml

This documentation is about how to use macro `create_model_yml` to create model yaml file. **_`snapshots`, `seeds`, `unit_tests`, `source` are not supported currently._**

change logs:

| version | author | since      | specification   |
| ------- | ------ | ---------- | --------------- |
| 0.0.1   | XZhang | 2025-08-15 | initial version |

### function parameters

To call this macro, you can use `dbt run-operation create_model_yml --args '{"model_name": "<model_name>"}'`. If you want to save the generated yml into a separate file, you can use `dbt --quiet run-operation create_model_yml --args '{"model_name": "<model_name>"}' | Out-File -FilePath "models\_test.yml" -Encoding utf8` for windows and `dbt --quiet run-operation create_model_yml --args '{"model_name": "<model_name>"}' > "models\_test.yml" ` for mac or linux.

### supported configurations

the whole configurations which used for creating a model yaml file are listed below and they should be located in `config` and within `meta` block.

```python
# optional
primary_keys: Union[None, str, list[str]] # defines the primary key (surrogate keys) of the table
model_description: Union[None, str] # model description
tags: Union[list[str], str, None] # model tags
cols: dict[str, dict[set[str], str], None] # the column information. The first key is the column name, the set can only be either description or data_type
schema_test: bool # define whether contract is activated or not
not_null_cols: Union[None, dict[str, str], list[str]] # defines which columns are not null and if it contains specific configuration. The supported parameters are [fail_calc, limit, severity, error_if, warn_if, store_failures, where]
unique_cols: Union[None, dict[str, str], list[str]] # defines which columns are unique and if it contains specific configuration. The supported parameters are [fail_calc, limit, severity, error_if, warn_if, store_failures, where]
accepted_values_cols: Union[None, dict[str, str]] # defines which values are accepted by the given column
not_accepted_values_cols: Union[None, dict[str, str]] # defines which values are not accepted by given column
accepted_range_cols: Union[None, dict[str, str]] # defines the accepted value range by given column. The supported parameters are [min_value, max_value, inclusive]
```

### Examples
#### 1. Full
```sql
{{ config(
    materialized = "table",
    meta = {
        "model_description": '{{ doc("clients_is_active") }}',
        "tags": ["tag1", "tag2", "tag3"],
        "primary_keys": ["key1", "key2"],
        "schema_test": "true", 
        "not_null_cols": ["col1", "col2", "col3", "col4"],
        "unique_cols": {
            "col3": {
                "fail_calc": "string",
                "limit": 1,
                "severity": "warn",
                "error_if": "string",
                "warn_if": "string",
                "store_failures": "false",
                "where": "conditional"
            },
            "col4": {}
        },
        "accepted_values_cols": {
            "status": {
                "values": ["placed", "shipped", "completed", "returned"],
                "fail_calc": "string",
                "limit": 1,
                "severity": "warn"
            }
        },
        "not_accepted_values_cols": {
            "status": {
                "values": ["broken"],
            }
        },
        "accepted_range_cols": {
            "num_col": {
                "min_value": 0,
                "max_value": 10,
                "inclusive": "false"
            }
        },
        "cols": {
            "key1": {
                "description": "key1",
                "data_type": "int"
            },
            "key2": {
                "description": "key2",
                "data_type": "int"
            },
            "col1": {
                "description": '{{ doc("clients_is_active") }}',
                "data_type": "int"
            },
            "col2": {
                "description": "col2",
                "data_type": "int"
            },
            "col3": {
                "description": "col3",
                "data_type": "int"
            },
            "col4": {
                "description": "col4",
                "data_type": "string"
            },
            "status": {
                "description": "status",
                "data_type": "string"
            },
            "num_col": {
                "data_type": "int"
            }
        }
    } 
) }}

select 
    1 as key1,
    2 as key2,
    3 as col1,
    4 as col2,
    5 as col3,
    6 as col4,
    9 as num_col,
    "completed" as status
```

created yml:
```yml
version: 2

models:
  - name: testcases
    description: '{{ doc("clients_is_active") }}'
    config:
      tags: ["tag1", "tag2", "tag3"]
      contract:
        enforced: true # if enforced = true, please keep in mind that all columns and its type have to be listed in cols meta
    data_tests:
      - dbt_utils.unique_combination_of_columns:
          combination_of_columns:
            - key1
            - key2
    columns:
      - name: col1
        description: '{{ doc("clients_is_active") }}'
        data_type: int
        data_tests:
          - not_null
      - name: col2
        description: col2
        data_type: int
        data_tests:
          - not_null
      - name: col3
        description: col3
        data_type: int
        data_tests:
          - not_null
          - unique:
              config:
                fail_calc: string
                limit: 1
                severity: warn
                error_if: string
                warn_if: string
                store_failures: false
                where: conditional
      - name: col4
        description: col4
        data_type: string
        data_tests:
          - not_null
          - unique
      - name: status
        description: status
        data_type: string
        data_tests:
          - accepted_values:
              values: ["placed", "shipped", "completed", "returned"]
              config:
                fail_calc: string
                limit: 1
                severity: warn
          - dbt_utils.not_accepted_values:
              values: ["broken"]
      - name: num_col
        data_type: int
        data_tests:
          - dbt_utils.accepted_range:
              min_value: 0
              max_value: 10
              inclusive: false
      - name: key1
        description: key1
        data_type: int
      - name: key2
        description: key2
        data_type: int
```

#### 2. If only one column is defined as primary key, the unique and not_null are activated instead of using dbt_utils.unique_combination_of_columns
```sql
{{ config(
    materialized = "table",
    meta = {
        "model_description": '{{ doc("clients_is_active") }}',
        "tags": ["tag1", "tag2", "tag3"],
        "primary_keys": ["key1"],
    } 
) }}

select 
    1 as key1,
    2 as key2,
    3 as col1,
    4 as col2,
    5 as col3,
    6 as col4,
    9 as num_col,
    "completed" as status
```

generated yml:
```yml
version: 2

models:
  - name: testcases
    description: '{{ doc("clients_is_active") }}'
    config:
      tags: ["tag1", "tag2", "tag3"]
    columns:
      - name: key1
        data_tests:
          - not_null:
              config:
                limit: 1
          - unique:
              config:
                limit: 1
```

#### 3. If schema_test is activated, please list all columns and its data_type, otherwise error will be thrown

```sql
{{ config(
    materialized = "table",
    meta = {
        "model_description": '{{ doc("clients_is_active") }}',
        "tags": ["tag1", "tag2", "tag3"],
        "primary_keys": ["key1"],
        "schema_test": "true"
    } 
) }}

select 
    1 as key1,
    2 as key2,
    3 as col1,
    4 as col2,
    5 as col3,
    6 as col4,
    9 as num_col,
    "completed" as status
```
In this dbt model, you activate _schema_test_, however no _data_type_ for column _key1_ is defined, `ERROR: All columns have to be listed with its data type in cols within meta, but got: None` is then thrown. 

corrected model:
```sql
{{ config(
    materialized = "table",
    meta = {
        "model_description": '{{ doc("clients_is_active") }}',
        "tags": ["tag1", "tag2", "tag3"],
        "primary_keys": ["key1"],
        "schema_test": "true",
        "cols": {
            "key1": {
                "description": "key",
                "data_type": "int"
            }
        }
    } 
) }}

select 
    1 as key1,
    2 as key2,
    3 as col1,
    4 as col2,
    5 as col3,
    6 as col4,
    9 as num_col,
    "completed" as status
```

generated_yml:
```yml
version: 2

models:
  - name: testcases
    description: '{{ doc("clients_is_active") }}'
    config:
      tags: ["tag1", "tag2", "tag3"]
      contract:
        enforced: true # if enforced = true, please keep in mind that all columns and its type have to be listed in cols meta
    constraints:
      - type: primary_key
        columns: key1
    columns:
      - name: key1
        description: key
        data_type: int
        data_tests:
          - not_null:
              config:
                limit: 1
          - unique:
              config:
                limit: 1
```

also, a small columns check is migrated. Which means, if you use _schema_test_ and the columns are not identical within _tests_ and _cols meta info_. An error will be thrown as well. 

```sql 
{{ config(
    materialized = "table",
    meta = {
        "model_description": '{{ doc("clients_is_active") }}',
        "tags": ["tag1", "tag2", "tag3"],
        "primary_keys": ["key1", "key2"],
        "schema_test": "true",
        "cols": {
            "key1": {
                "description": "key",
                "data_type": "int"
            }
        }
    } 
) }}

select 
    1 as key1,
    2 as key2,
    3 as col1,
    4 as col2,
    5 as col3,
    6 as col4,
    9 as num_col,
    "completed" as status
```
the primary keys are _key1_, and _key2_. But only _key1_ is defined with _schema_test_. The `ERROR: You do not list all columns or its data type in meta cols` is then thrown. 

#### 4. If schema_test is deactivated, but data_type is found within cols. The expectation test will be automatically added

```sql
{{ config(
    materialized = "table",
    meta = {
        "model_description": '{{ doc("clients_is_active") }}',
        "tags": ["tag1", "tag2", "tag3"],
        "primary_keys": ["key1", "key2"],
        "cols": {
            "key1": {
                "description": "key",
                "data_type": "int"
            }
        }
    } 
) }}

select 
    1 as key1,
    2 as key2,
    3 as col1,
    4 as col2,
    5 as col3,
    6 as col4,
    9 as num_col,
    "completed" as status
```

generated yml:
```yml
version: 2

models:
  - name: testcases
    description: '{{ doc("clients_is_active") }}'
    config:
      tags: ["tag1", "tag2", "tag3"]
    constraints:
      - type: primary_key
        columns: [key1, key2]
    data_tests:
      - dbt_utils.unique_combination_of_columns:
          combination_of_columns:
            - key1
            - key2
    columns:
      - name: key1
        description: key
        data_tests:
          - dbt_expectations.expect_column_values_to_be_of_type: # use expect_column_values_to_be_of_type only neccessary
              column_type: int
      - name: key2
```

Futher tests and usecases could be added. 

### Others
in order to make this creation macro without problem, please install `dbt_utils` and `dbt_expectation` dependencies. Otherwise this macro works with limitations. 

Besides, please ensure that all values in config block are based type (either string or int). 