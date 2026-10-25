"""Zero-dependency SQL Interview Practice Runner (uses Python standard library sqlite3)."""

import sqlite3
from typing import Any, List, Tuple


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    setup_schema_and_data(conn)
    return conn


def setup_schema_and_data(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()

    # 1. Employees table for ranking / salary / lag/lead
    cur.execute(
        """
        CREATE TABLE employees (
            emp_id INT PRIMARY KEY,
            emp_name TEXT,
            dept_id INT,
            department TEXT,
            salary INT,
            hire_date DATE
        );
        """
    )
    cur.executemany(
        "INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?);",
        [
            (1, "Alice", 101, "Engineering", 120000, "2021-03-01"),
            (2, "Bob", 101, "Engineering", 120000, "2020-01-15"),
            (3, "Charlie", 101, "Engineering", 95000, "2022-06-01"),
            (4, "Diana", 101, "Engineering", 80000, "2023-08-10"),
            (5, "Evan", 102, "Sales", 110000, "2019-11-05"),
            (6, "Fiona", 102, "Sales", 110000, "2021-04-12"),
            (7, "George", 102, "Sales", 90000, "2022-09-20"),
            (8, "Hannah", 103, "Marketing", 95000, "2020-07-01"),
            (9, "Ian", 103, "Marketing", 85000, "2021-12-15"),
        ],
    )

    # 2. Daily revenue for running totals / moving windows
    cur.execute(
        """
        CREATE TABLE daily_sales (
            sale_date DATE PRIMARY KEY,
            amount INT
        );
        """
    )
    cur.executemany(
        "INSERT INTO daily_sales VALUES (?, ?);",
        [
            ("2026-01-01", 100),
            ("2026-01-02", 150),
            ("2026-01-03", 200),
            ("2026-01-04", 120),
            ("2026-01-05", 300),
            ("2026-01-06", 250),
            ("2026-01-07", 180),
        ],
    )

    # 3. User logins for retention / streaks / lag
    cur.execute(
        """
        CREATE TABLE user_logins (
            user_id INT,
            login_date DATE
        );
        """
    )
    cur.executemany(
        "INSERT INTO user_logins VALUES (?, ?);",
        [
            (1, "2026-01-01"),
            (1, "2026-01-02"),
            (1, "2026-01-03"),
            (2, "2026-01-01"),
            (2, "2026-01-03"),
            (3, "2026-01-02"),
            (3, "2026-01-03"),
            (3, "2026-01-04"),
        ],
    )

    # 4. Duplicate event records for deduplication pattern
    cur.execute(
        """
        CREATE TABLE event_logs (
            event_id INT,
            user_id INT,
            action TEXT,
            updated_at TIMESTAMP
        );
        """
    )
    cur.executemany(
        "INSERT INTO event_logs VALUES (?, ?, ?, ?);",
        [
            (101, 1, "view", "2026-01-01 10:00:00"),
            (101, 1, "view", "2026-01-01 10:05:00"),
            (102, 2, "click", "2026-01-01 11:00:00"),
            (103, 1, "purchase", "2026-01-01 12:00:00"),
            (103, 1, "purchase", "2026-01-01 12:02:00"),
        ],
    )

    conn.commit()


def run_query(conn: sqlite3.Connection, query: str) -> List[Tuple[Any, ...]]:
    cur = conn.cursor()
    cur.execute(query)
    return [tuple(row) for row in cur.fetchall()]
