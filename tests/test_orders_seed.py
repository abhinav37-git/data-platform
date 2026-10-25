"""Checks the source seed that dbt and Debezium both read."""

from pathlib import Path


def test_init_sql_creates_orders() -> None:
    sql = Path("sql/init.sql").read_text()
    assert "create table if not exists public.orders" in sql
    assert "analytics_pub" in sql
