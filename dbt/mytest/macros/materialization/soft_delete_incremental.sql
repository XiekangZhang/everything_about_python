{# 
the custom materialization for bigquery adapter. It could be possible used for other adapter. 
But no tests are done yet, please take it at your own risks. 

change log:
0.0.1: initial version

@author: XZhang
@version: 0.0.1
@since: 2025-07-07
#}

{% materialization soft_delete_incremental, adapter = 'bigquery' %}
    {% set target_relation = this %}
    {% set unique_key = config.get('unique_key') %}
    {% set delete_column_name = config.get('delete_column_name') %}

    {% set partition_by = config.get('partition_by') %}
    {% set cluster_by = config.get('cluster_by') %}
    {% set incremental_predicates = config.get('incremental_predicates') %}

    {% set soft_delete_enabled = var('enable_soft_deletes', false) %}

    {% if unique_key is not string and unique_key is not iterable %}
        {{ exceptions.raise_compiler_error("ERROR: unique_key must be a string or a list of strings.") }}
    {% endif %}
    {% if unique_key is string %}
        {% set unique_key = [unique_key] %}
    {% endif %}
    {% set unique_key = unique_key | map('lower') | list %}


    {% if cluster_by is string %}
        {% set cluster_by = [cluster_by] %}
    {% endif %}
    {% set cluster_by = cluster_by | map('lower') | list %}

    {% if incremental_predicates is string %}
        {% set incremental_predicates = [incremental_predicates] %}
    {% endif %}

    {% if not delete_column_name %}
        {{ exceptions.raise_compiler_error("ERROR: delete_column_name is mandatory for this materialization.") }}
    {% endif %}
    {% if delete_column_name is not string %}
        {{ exceptions.raise_compiler_error("ERROR: delete_column_name should be a string.") }}
    {% endif %}

    {% set existing_relation = load_relation(this) %}
    {% set model_columns = get_columns_in_query(model['compiled_code']) %}
    {% set model_column_names = model_columns | map('lower') | list %}

    {% set target_model_columns = adapter.get_columns_in_relation(target_relation) %}
    {% set target_model_column_names = target_model_columns | map(attribute='name') | map('lower') | list %}

    {% if should_full_refresh() %}
        {{ exceptions.warn("WARN: full_refresh flag is currently not supported. This flag will be ignored.") }}
    {% endif %}

    {% if not existing_relation %}
        {{ log("INFO: creating target table" ~ target_relation, info=true) }}
        -- Case 1: Target table does not exist
        {% call statement('main') %}
        CREATE OR REPLACE TABLE {{ target_relation }}
        {% if partition_by %}
        PARTITION BY 
            {% if partition_by.data_type | lower == 'date' %}
            DATE_TRUNC({{ partition_by.field }}, 
                {% if partition_by.granularity | lower == 'month' %} 
                MONTH
                {% elif partition_by.granularity | lower == 'year' %}
                YEAR
                {% else %}
                {{ exceptions.raise_compiler_error("ERROR: only month, year is accepted.") }}
                {% endif %}
            )
            {% elif partition_by.data_type | lower == 'timestamp' %}
            TIMESTAMP_TRUNC({{ partition_by.field }}, 
                {% if partition_by.granularity | lower == 'day' %}
                DAY 
                {% elif partition_by.granularity | lower == 'month' %} 
                MONTH
                {% elif partition_by.granularity | lower == 'year' %}
                YEAR
                {% elif partition_by.granularity | lower == 'hour' %}
                HOUR
                {% else %}
                {{ exceptions.raise_compiler_error("ERROR: only day, month, year, hour is accepted.") }}
                {% endif %}
            )
            {% elif partition_by.data_type | lower == 'int64' %}
                {% if not partition_by.range %} 
                    {{ exceptions.raise_compiler_error("ERROR: range object is mandatory for int64 data_type.") }}
                {% endif %}
            RANGE_BUCKET({{ partition_by.field }}, GENERATE_ARRAY({{ partition_by.range.start }}, {{ partition_by.range.end }}, {{ partition_by.range.interval }}))
            {% else %}
            {{ exceptions.raise_compiler_error("ERROR: only date, timestamp, int64 is accepted.") }}
            {% endif %}
        {% endif %}

        {% if cluster_by %}
        CLUSTER BY {{ cluster_by | join(', ')}}
        {% endif %}
        AS (
            WITH source_data AS (
            {{ model['compiled_code'] }}
            )
            SELECT 
                {% for col in model_column_names %}
                    {{ col }},
                {% endfor %}
                false AS {{ delete_column_name | lower }},
                CURRENT_TIMESTAMP() AS __last_updated_time
            FROM source_data
        );
        {% endcall %}

    {% else %}
    {{ log('INFO: Target table ' ~ target_relation ~ ' already exists. Proceeding with MERGE.', info=true) }}
    -- Case 2: Target table exists, so merge
    {% call statement('main') %}

    MERGE {{ target_relation }} AS T
    USING ( 
        WITH source_data AS (
            {{ model['compiled_code'] }}
        )
        SELECT 
            {% for col in model_column_names %}
                {{ col }},
            {% endfor %}
            false AS {{ delete_column_name | lower }}
        FROM source_data
    ) AS S
    ON (
        {% if incremental_predicates and not soft_delete_enabled %} {{ incremental_predicates | join('AND ') }} AND {% endif %}
        {% for key in unique_key %}
        T.{{ key }} = S.{{ key }}
        {% if not loop.last %} AND {% endif %}
        {% endfor %}
    )
    -- Update
    WHEN MATCHED THEN UPDATE SET 
        {% for col in model_column_names if col not in unique_key and col in target_model_column_names %}
            T.{{ col }} = S.{{ col }},
        {% endfor %}
        T.{{ delete_column_name | lower }} = false
    -- Insert
    WHEN NOT MATCHED BY TARGET THEN INSERT (
        {% for col in model_column_names if col in target_model_column_names %}
            {{ col }},
        {% endfor %}
        {{ delete_column_name | lower }},
        __last_updated_time
    ) VALUES (
        {% for col in model_column_names if col in target_model_column_names %}
            S.{{ col }},
        {% endfor %}
        false,
        CURRENT_TIMESTAMP()
    )
    -- soft deletion
    {% if soft_delete_enabled %}
    WHEN NOT MATCHED BY SOURCE THEN UPDATE SET
        T.{{ delete_column_name | lower }} = true,
        __last_updated_time = CURRENT_TIMESTAMP()
    {% endif %}
    {% endcall %}
    
    {% endif %}
    {{ return({'relations': [target_relation]}) }}

{% endmaterialization %}
