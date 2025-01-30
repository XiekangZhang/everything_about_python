{% for i in range(10) %}
    SELECT {{i}} as number {% if not loop.last %} union all {% endif %}
{% endfor %}