{{ config(
    materialized = 'table'
) }}

WITH customers AS (

    SELECT
        customer_id,
        first_name,
        last_name
    FROM
        `xiekang-playground.playground.customers`
),
orders AS (
    SELECT
        id AS order_id,
        user_id AS customer_id,
        order_date,
        status
    FROM
        `xiekang-playground.playground.orders`
),
customer_orders AS (
    SELECT
        customer_id,
        MIN(order_date) AS first_order_date,
        MAX(order_date) AS most_recent_order_date,
        COUNT(order_id) AS number_of_orders
    FROM
        orders
    GROUP BY
        1
),
FINAL AS (
    SELECT
        customers.customer_id,
        customers.first_name,
        customers.last_name,
        customer_orders.first_order_date,
        customer_orders.most_recent_order_date,
        COALESCE(
            customer_orders.number_of_orders,
            0
        ) AS number_of_orders
    FROM
        customers
        LEFT JOIN customer_orders USING (customer_id)
)
SELECT
    *
FROM
    FINAL
