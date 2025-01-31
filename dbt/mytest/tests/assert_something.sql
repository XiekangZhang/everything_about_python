SELECT
    order_date
FROM
    {{ ref("stg_jaffle_shop__orders") }}
GROUP BY
    1
HAVING
    order_date >= CURRENT_DATE()
