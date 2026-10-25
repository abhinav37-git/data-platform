#!/usr/bin/env python3
"""Interactive SQL practice tool.

Usage:
    python3 sql/practice.py
"""

import sys
from sql.practice_harness import get_connection, run_query


CHALLENGES = [
    {
        "id": 1,
        "title": "Nth Highest Salary per Department (Window Ranking)",
        "concepts": "DENSE_RANK() vs RANK() vs ROW_NUMBER(), PARTITION BY",
        "question": "Find the 2nd highest salary in each department. If two employees tie for 1st place, the next distinct salary should be rank 2 (no gap). Return: department, emp_name, salary, rnk",
        "starter_sql": """-- Write your query here
SELECT
    department,
    emp_name,
    salary,
    1 as rnk
FROM employees
LIMIT 5;
""",
    },
    {
        "id": 2,
        "title": "Cumulative Total & Rolling Window",
        "concepts": "ROWS BETWEEN ... PRECEDING AND CURRENT ROW",
        "question": "Calculate daily cumulative sales AND a 3-day rolling sales sum (current day + previous 2 days). Return: sale_date, amount, cumulative_sales, rolling_3d_sales",
        "starter_sql": """-- Write your query here
SELECT
    sale_date,
    amount
FROM daily_sales;
""",
    },
    {
        "id": 3,
        "title": "Deduplication / Latest Record per Entity",
        "concepts": "ROW_NUMBER() with PARTITION BY ... ORDER BY ... DESC",
        "question": "In event_logs, multiple rows exist for the same event_id due to updates. Pick only the most recent record per event_id. Return: event_id, user_id, action, updated_at",
        "starter_sql": """-- Write your query here
SELECT * FROM event_logs;
""",
    },
    {
        "id": 4,
        "title": "Gaps & Islands: Consecutive Streaks",
        "concepts": "DATE arithmetic + ROW_NUMBER() grouping trick",
        "question": "Find all user_ids who logged in for at least 3 consecutive days. Return: user_id",
        "starter_sql": """-- Write your query here
SELECT DISTINCT user_id FROM user_logins;
""",
    },
    {
        "id": 5,
        "title": "Period-over-Period Growth / Delta",
        "concepts": "LAG() / LEAD() with ORDER BY",
        "question": "Compare daily amount with previous day's amount and calculate the numeric difference. Return: sale_date, amount, prev_day_amount, diff",
        "starter_sql": """-- Write your query here
SELECT
    sale_date,
    amount
FROM daily_sales;
""",
    },
]


def main():
    print("=" * 60)
    print("  DATA ENGINEERING SQL INTERVIEW PRACTICE LAB")
    print("=" * 60)
    print("Available Challenges:")
    for ch in CHALLENGES:
        print(f"  [{ch['id']}] {ch['title']} ({ch['concepts']})")
    print("-" * 60)
    print("To test and verify solutions against the automated harness, run:")
    print("  PYTHONPATH=. pytest tests/test_sql_challenges.py -v\n")


if __name__ == "__main__":
    main()
