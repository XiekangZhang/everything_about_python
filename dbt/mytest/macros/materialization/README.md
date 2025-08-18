# Introduction to custom materialization - soft_delete_incremental

according to our requirements, a new custom materialization for dbt was developed, which is called **soft_delete_incremental**. Unlike the normal incremental materialization, it provides a new feature, namely marking the rows as deleted if it does not exist in the source anymore. If you want to use this feature, you need to activate it by changing the global variable `enable_soft_deletes: true` or passing this variable with your dbt commands `dbt xxx --vars 'enable_soft_deletes: true'`.

Changelogs:

| version | author | since      | description                                        |
| ------- | ------ | ---------- | -------------------------------------------------- |
| 0.0.1   | XZhang | 2025-07-07 | initial version with focus on **bigquery** adapter |

Specification in version 0.0.1:

the following configuration parameters are accepted by using this materialization:

```python
# mandatory configuration parameters:
unique_key: Union[str, list[str]] # the unique_key from source
delete_column:name: str # the column name used to mark whether the row is deleted in source or not

# optional configuration parameters:
partition_by: Optional[dict[str, str]] # the partition column used for creating the table, if the table does not exist. Only following structures are allowed:
'''
{
    'field': '<name of the column>',
    'data_type': '<date|timestamp|int64>',
    # case 1: mandatory if data_type = date
    'granularity': '<day|month>'
    # case 2: mandatory if data_type = timestamp
    'granularity': '<day|month|year|hour>'
    # case 3: mandatory if data_type = int64
    'range': {
        'start': <int>,
        'end': <int>,
        'interval': <int>
    }
}
concrete example:
{ 'field': '_extracted_at',
  'data_type': 'timestamp',
  'granularity': 'day' }
{ 'field': 'year',
  'data_type': 'int64',
  'range': {
    'start': 2000,
    'end': 2999,
    'interval': 1
  }
}
'''
cluster_by: Union[str, list[str]] # the cluster column used for creating the table
incremental_predicates: Union[str, list[str]] # the conditions used to select the right data
```

one example to use this custom materialization with the configuration parameters:

```jinja2
{{ config(
    materialized = 'soft_delete_incremental',
    unique_key = ['lfdnr'],
    delete_column_name = '_is_deleted_in_source',
    partition_by ={ 'field': '_extracted_at',
    'data_type': 'timestamp',
    'granularity': 'day' },
    cluster_by = ['_extracted_at'],
    incremental_predicates = ['T._extracted_at > S.dest_date']
) }}
```

this custom materialization should work with `is_soft_delete_incremental()` macro together. This macro will check 3 things - table existance, soft_delete_incremental materialization used, and enable_soft_deletes. You can add conditions to select source, or/and target table within `if is_soft_delete_incremental()` to reduce the scanned data size.

unit test (done):

1. creating table with different configuration parameters (with partition_by, with cluster_by, with both)
2. creating table with different partition_by data_type and granularity or range
3. merging table when enable_soft_deletes deactivates and when enable_soft_deletes activates
4. testing with incremental_predicators
5. 'deleted rows' back to active
