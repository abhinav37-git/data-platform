create table if not exists public.orders (
    order_id bigint primary key,
    customer_id bigint not null,
    amount numeric(12, 2) not null,
    ordered_at timestamptz not null default now()
);

insert into public.orders (order_id, customer_id, amount)
values
    (1, 10, 25.00),
    (2, 11, 40.50),
    (3, 10, 15.25)
on conflict (order_id) do nothing;

do $$
begin
    if not exists (select 1 from pg_publication where pubname = 'analytics_pub') then
        create publication analytics_pub for table public.orders;
    end if;
    if exists (select 1 from pg_roles where rolname = 'debezium') then
        grant select on public.orders to debezium;
    end if;
end $$;
