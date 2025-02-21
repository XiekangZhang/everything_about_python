{#
{% for i in range(10) %}
SELECT
    {{ i }} AS NUMBER {% if not loop.last %}
    UNION ALL
    {% endif %}
{% endfor %}
#}

{% set my_animals = ['lemur', 'wolf', 'panther', 'tardigrade'] %}
select 'my favirite animal is the {{my_animals[0]}}'

