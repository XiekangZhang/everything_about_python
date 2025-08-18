{# 
this macro is used to create either incremental model or soft_delete_incremental with current best practise for dbt. 
it can only be used if you do not have any transformation in the column and the columns which used for conditions are time-based, e.g., date, timestamp, or datetime.
if you have some additional transformation or the mentioned columns have different data type, please write your own ctes.

@author: XZhang
@version: 0.0.1
@since: 2025-07-07
#}


{% macro create_basic_incremental_model(source_relation, target_relation, time_filter_col, source_filter_time_column_name='dest_date') %}
    {% set mode = var('enable_soft_deletes', false) %}
    {% set source_columns_object = adapter.get_columns_in_relation(source_relation) %}
    {% set source_columns_names = source_columns_object | map(attribute='name') | map('lower') | list %}
    {% set unique_key = config.get('unique_key') %}
    {% set partition_by_column = config.get('partition_by') %}
    {% set mode = config.get('materialized') %}
    {% set existing_relation = load_relation(target_relation) %}


    {% if unique_key is string %}
        {% set unique_key = [unique_key] %}
    {% endif %}

    {% set basic_incremental_model %}
        WITH source AS (
            SELECT 
                {% for col in source_columns_names %}
                {{ col }}
                {% if not loop.last %}, {% endif %}
                {% endfor %}
            FROM {{ source_relation }}
        {% if mode == 'incremental' %} 
            {% if existing_relation %}
            {%- set max_time_filter_col_query -%}
                SELECT
                    MAX(TIMESTAMP_SUB(TIMESTAMP({{ time_filter_col }}), INTERVAL 3 DAY))
                FROM
                    {{ target_relation }}
                {%- endset -%}
                {%- set max_time_filter_col = run_query(max_time_filter_col_query).columns [0].values() [0] -%}
            WHERE
                {{ time_filter_col }} > '{{ max_time_filter_col }}'
            {% endif %}
            QUALIFY ROW_NUMBER() over (
                PARTITION BY {{unique_key | join(', ') }}
                ORDER BY {{time_filter_col}} DESC
            ) = 1
        ),       
            {% if existing_relation %}
        dest AS (
            SELECT 
                MAX(TIMESTAMP_SUB(TIMESTAMP({{ partition_by_column.field }}), INTERVAL 1095 DAY)) AS {{ source_filter_time_column_name }}
            FROM {{ target_relation }}),
            final AS (
                SELECT source.*, dest.*
                FROM source, dest
            )
            {% else %}
            final AS (
                SELECT *
                FROM source
                )
            {% endif %}
            SELECT *
            FROM final

        {% elif mode == 'soft_delete_incremental' %}
        {% if existing_relation and var('enable_soft_deletes') == false %}
            {%- set max_time_filter_col_query -%}
                SELECT
                    MAX(TIMESTAMP_SUB(TIMESTAMP({{ time_filter_col }}), INTERVAL 3 DAY))
                FROM
                    {{ target_relation }}
                {%- endset -%}
                {%- set max_time_filter_col = run_query(max_time_filter_col_query).columns [0].values() [0] -%}
            WHERE
                {{time_filter_col}} > '{{ max_time_filter_col }}'
            {% endif %}
            QUALIFY ROW_NUMBER() over (
                PARTITION BY {{unique_key | join(', ') }}
                ORDER BY {{time_filter_col}} DESC
            ) = 1
        ),       
            {% if existing_relation and var('enable_soft_deletes') == false %}
        dest AS (
            SELECT 
                MAX(TIMESTAMP_SUB(TIMESTAMP({{ partition_by_column.field }}), INTERVAL 1095 DAY)) AS {{ source_filter_time_column_name }}
            FROM {{ target_relation }}),
            final AS (
                SELECT source.*, dest.*
                FROM source, dest
            )
            {% else %}
            final AS (
                SELECT *
                FROM source
                )
            {% endif %}
            SELECT *
            FROM final
        {% endif %}
    {% endset %}
    {{ return(basic_incremental_model) }}
{% endmacro %}