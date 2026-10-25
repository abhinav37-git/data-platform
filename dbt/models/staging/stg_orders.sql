with source as (

    select
        order_id,
        customer_id,
        amount,
        ordered_at
    from {{ source('app', 'orders') }}

)

select
    order_id,
    customer_id,
    amount,
    ordered_at
from source
