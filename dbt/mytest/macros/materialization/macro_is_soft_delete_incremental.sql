{% macro is_soft_delete_incremental() %}
    {% set existing_relation = load_relation(this) %}
    {{ return(existing_relation 
        and config.get('materialized') == 'soft_delete_incremental'
        and var('enable_soft_deletes') == false
        ) }}
{% endmacro %}