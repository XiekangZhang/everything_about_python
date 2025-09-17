{% macro create_model_yml(model_name) %}
    {% set model_node = graph.nodes.values() 
        | selectattr("resource_type", "equalto", "model") 
        | selectattr("name", "equalto", model_name)
        | first
    %}
    {% if not model_node %}
        {{ exceptions.raise_compiler_error("ERROR: Invalid Model Name. Got: " ~ model_name) }}
    {% endif %}

    -- mandatory
    {% set meta = model_node.config.meta %}
    {% if not meta %}
        {{ exceptions.raise_compiler_error("ERROR: META Info is mandatory, but got: " ~ meta) }}
    {% endif %}

    -- optional
    {% set primary_keys = meta.primary_keys %}
    {% if primary_keys and primary_keys is sequence and primary_keys | length == 1 %}
        {% set primary_keys = primary_keys[0] %}
    {% endif %}

    {% set model_description = meta.model_description %}
    {% set tags = meta.tags %}
    {% if tags and tags is string %}
        {% set tags = [tags] %}
    {% endif %}

    {% set cols = meta.cols %}
    {% if not cols %}
    {% set cols = {} %}
    {% endif %}

    {% set schema_test = meta.schema_test %}
    {% if not schema_test %}
    {% set schema_test = 'false' %}
    {% endif %}
    
    {% set not_null_cols = meta.not_null_cols %}
    {% if not not_null_cols %}
    {% set not_null_cols = {} %}
    {% endif %}

    {% set unique_cols = meta.unique_cols %}
    {% if not unique_cols %}
    {% set unique_cols = {} %}
    {% endif %}

    {% set accepted_values_cols = meta.accepted_values_cols %}  
    {% if not accepted_values_cols %}
    {% set accepted_values_cols = {} %}
    {% endif %}

    {% set not_accepted_values_cols = meta.not_accepted_values_cols %}
    {% if not not_accepted_values_cols %}
    {% set not_accepted_values_cols = {} %}
    {% endif %}

    {% set accepted_range_cols = meta.accepted_range_cols %}
    {% if not accepted_range_cols %}
    {% set accepted_range_cols = {} %}
    {% endif %}

    {% set test_map = {
                    "not_null": "not_null",
                    "unique": "unique",
                    "accepted_values": "accepted_values",
                    "not_accepted_values": "dbt_utils.not_accepted_values", 
                    "accepted_range": "dbt_utils.accepted_range", 
                    "expect_column_values_to_be_of_type": "dbt_expectations.expect_column_values_to_be_of_type"
                    } %}

    -- validation
    --- not null
    {% if not_null_cols and not_null_cols is not mapping %}
        {% set not_null_cols_dict = {} %}
        {% for col in not_null_cols %}
            {% do not_null_cols_dict.update({col: None}) %}
        {% endfor %}
        {% set not_null_cols = not_null_cols_dict %}
    {% endif %}
    {% if primary_keys is string %}
        {% do not_null_cols.update({primary_keys: {"limit": 1}}) %}
    {% endif %}
    --- unique
    {% if unique_cols and unique_cols is not mapping %}
        {% set unique_cols_dict = {} %}
        {% for col in unique_cols %}
            {% do unique_cols_dict.update({col: None}) %}
        {% endfor %}
        {% set unique_cols = unique_cols_dict %}
    {% endif %}
    {% if primary_keys is string %}
        {% do unique_cols.update({primary_keys: {"limit": 1}}) %}
    {% endif %}
    --- accepted values
    {% if accepted_values_cols and accepted_values_cols is not mapping %}
        {{ exceptions.raise_compiler_error("ERROR: accepted_values_cols has to be object type, but got: " ~ accepted_values_cols) }}
    {% endif %}
    --- not accepted values
    {% if not_accepted_values_cols and not_accepted_values_cols is not mapping %}
        {{ exceptions.raise_compiler_error("ERROR: not_accepted_values_cols has to be object type, but got: " ~ not_accepted_values_cols) }}
    {% endif %}
    --- accepted range
    {% if accepted_range_cols and accepted_range_cols is not mapping %}
        {{ exceptions.raise_compiler_error("ERROR: accepted_range_cols has to be object type, but got: " ~ accepted_range_cols) }}
    {% endif %}
    --- expect_column_values_to_be_of_type
    {% set expect_column_values_to_be_of_type_cols = {} %}
    {% if schema_test and schema_test | lower == "false" %}
        {% if cols %}
            {% for col, col_config in cols.items() %}
                {% if col_config.data_type %}
                    {% do expect_column_values_to_be_of_type_cols.update({col: col_config.data_type}) %}
                {% endif %}
            {% endfor %}
        {% endif %}
    {% elif schema_test and schema_test | lower == "true" %}
        {% if not cols %}
            {{ exceptions.raise_compiler_error("ERROR: All columns have to be listed with its data type in cols within meta, but got: " ~ None) }}
        {% endif %}
    {% endif %}

    {% set cols_tests_config = __prepare_test_config(
            not_null=not_null_cols, 
            unique=unique_cols, 
            accepted_values=accepted_values_cols, 
            not_accepted_values=not_accepted_values_cols, 
            accepted_range=accepted_range_cols,
            expect_column_values_to_be_of_type=expect_column_values_to_be_of_type_cols
        ) 
    %}
   
    {% if primary_keys is not string %}
        {% for primary_key in primary_keys %}
            {% if primary_key not in cols_tests_config.keys() %}
                {% do cols_tests_config.update({primary_key: {}}) %}
            {% endif %}
        {% endfor %}
    {% endif %}
    
{%- set generated_yml -%}
    {{ _generate_yaml_header() }}
    {{ _generate_models_level_configuration(model_name, model_description, tags, schema_test, primary_keys) -}}
    {%- if cols_tests_config -%}
    {{ _generate_columns_level_configuration(cols, cols_tests_config, schema_test, test_map) }}
    {%- endif -%}
{%- endset -%}
{{ print(generated_yml) }}
{{ return(generated_yml) }}
{% endmacro %}



{%- macro __prepare_test_config() -%}
    {% set cols_tests_config = {} %}
    {% for test_type, test_info in kwargs.items() %}
        {% if test_info %}
            {% for col, config in test_info.items() %}
                {% if col not in cols_tests_config.keys() %}
                    {% do cols_tests_config.update({col: [{test_type: config}]}) %}
                {% else %}
                    {{ cols_tests_config.get(col).append({test_type: config}) }}                    
                {% endif %}
            {% endfor %}
        {% endif %}
    {% endfor %}
    {{ return(cols_tests_config) }}
{%- endmacro -%}



{%- macro _generate_yaml_header() -%}
# --------------------------------------------------------------------------------------------#
# WARNING: DO NOT EDIT THIS FILE MANUALLY.                                                    #
# This file is automatically generated by the `create_model_yml` macro.                       #
# To make changes, edit the `meta` block in the model sql file and re-run this macro.         #
# Feel free to add new features with documentation                                            #
# Last generated on: {{ modules.datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') }}                                                      #
# --------------------------------------------------------------------------------------------#
{%- endmacro -%}



{%- macro _generate_models_level_configuration(model_name, model_description, tags, schema_test, primary_keys, indent_level= 2) -%}
{%- set root_level = ' ' * 1 * indent_level -%}
{%- set level1 = ' ' * 2 * indent_level -%}
{%- set level2 = ' ' * 3 * indent_level -%}
{%- set level3 = ' ' * 4 * indent_level -%}
{%- set level4 = ' ' * 5 * indent_level -%}
{%- set level5 = ' ' * 6 * indent_level %}
version: 2

models:
{{ root_level }}- name: {{ model_name }}
{%- if model_description %}
{{ level1 }}description: {% if '{{' in model_description and '}}' in model_description and '"' in model_description -%} {{ "'" ~ model_description ~ "'" }}  {%- elif '{{' in model_description and '}}' in model_description and "'" in model_description -%} {{ '"' ~ model_description ~ '"' }} {%- else -%} {{ model_description }} {%- endif %}
{%- endif -%}
{%- if tags or schema_test | lower == "true" %}
{{ level1 }}config:
{%- endif -%}
{%- if tags %}
{{ level2 }}tags: {{ tags | string | replace("'", '"') }} 
{%- endif -%}
{%- if schema_test and schema_test | lower == "true" %}
{{ level2 }}contract:
{{ level3 }}enforced: {{ schema_test | lower }} # if enforced = true, please keep in mind that all columns and its type have to be listed in cols meta
{%- endif -%}
{%- if primary_keys %}
{{ level1 }}constraints:
{{ level2 }}- type: primary_key
{{ level3 }}columns: {{ primary_keys | string | replace("'", "") | replace('"', '') }}
{%- endif -%}
{%- if primary_keys is not string and primary_keys | length >= 2 %}
{{ level1 }}data_tests:
{{ level2 }}- dbt_utils.unique_combination_of_columns:
{{ level4 }}combination_of_columns:
{%- for key in primary_keys %}
{{ level5 }}- {{ key }}
{%- endfor -%}
{%- endif -%}
{%- endmacro -%}



{%- macro _generate_columns_level_configuration(cols, cols_tests_config, schema_test, test_map, indent_level= 2) -%}
{%- set flag = namespace(a=1) -%}
{%- set level1 = ' ' * 2 * indent_level -%}
{%- set level2 = ' ' * 3 * indent_level -%}
{%- set level3 = ' ' * 4 * indent_level -%}
{%- set level4 = ' ' * 5 * indent_level -%}
{%- set level5 = ' ' * 6 * indent_level -%}
{%- set level6 = ' ' * 7 * indent_level -%}
{%- set level7 = ' ' * 8 * indent_level %}
{{ level1 }}columns:
{%- for col in cols.keys() %}
{{ level2 }}- name: {{ col }}
{%- if cols and cols.get(col).description %}
{{ level3 }}description: {% if '{{' in cols.get(col).description and '}}' in cols.get(col).description and '"' in cols.get(col).description -%} {{ "'" ~ cols.get(col).description ~ "'" }}  {%- elif '{{' in cols.get(col).description and '}}' in cols.get(col).description and "'" in cols.get(col).description -%} {{ '"' ~ cols.get(col).description ~ '"' }} {%- else -%} {{ cols.get(col).description }} {%- endif %}
{%- endif -%}
{%- if schema_test | lower == "true" %}
{%- if cols and cols.get(col).data_type %}
{{ level3 }}data_type: {{ cols.get(col).data_type }}
{%- else -%}
{{ exceptions.raise_compiler_error("ERROR: You do not list all columns or its data type in meta cols") }}
{%- endif -%}
{%- endif -%}
{%- if cols_tests_config.get(col) %}
{{ level3 }}data_tests:
{%- for tests_config in cols_tests_config.get(col) -%}
{%- for test_type, test_config in tests_config.items() %}
{{ level4 }}- {{ test_map.get(test_type) }}
{%- if schema_test | lower == "false" and test_type | lower == "expect_column_values_to_be_of_type" %}
{%- if cols.get(col).data_type -%}
: # use expect_column_values_to_be_of_type only neccessary
{{ level6 }}column_type: {{ cols.get(col).data_type }}  
{%- endif -%}
{%- endif -%}
{%- if test_config and test_config is mapping -%}
:
{%- if "max_value" in test_config.keys() or "min_value" in test_config.keys() or "inclusive" in test_config.keys() or "values" in test_config.keys() -%}
{%- for k, v in test_config.items() %}
{%- if k in ["values", "min_value", "max_value", "inclusive"] %}
{{ level6 }}{{ k }}: {{ v | string | replace("'", '"') }}
{%- elif flag.a == 1 %}
{{ level6 }}config:
{{ level7 }}{{ k }}: {{ v }}
{%- set flag.a = 2 -%}
{%- elif flag.a == 2 %}
{{ level7 }}{{ k }}: {{ v }}
{%- endif -%}
{%- endfor -%}
{%- else %}
{{ level6 }}config:
{%- for k, v in test_config.items() %}
{{ level7 }}{{ k }}: {{ v }}
{%- endfor -%}
{%- endif -%}
{%- endif -%}
{%- endfor -%}
{%- endfor -%}
{%- endif -%}
{%- endfor %}
{%- endmacro -%}