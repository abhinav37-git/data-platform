"""Unit test suite verifying SQL practice solutions.

Run via:
    pytest tests/test_sql_challenges.py -v
"""

from sql.practice_harness import get_connection, run_query


# Challenge 1: Find the 2nd highest salary in each department.
# In case of ties, both employees should share the rank, without skipping rank numbers.
# Expected columns: department, emp_name, salary, rnk
CHALLENGE_1_SQL = """
-- Write your SQL query below:
SELECT
    department,
    emp_name,
    salary,
    rnk
FROM (
    SELECT
        department,
        emp_name,
        salary,
        DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS rnk
    FROM employees
) t
WHERE rnk = 2
ORDER BY department, emp_name;
"""


# Challenge 2: Running 3-day rolling sum and cumulative total of daily sales.
# Columns: sale_date, amount, cumulative_sales, rolling_3d_sales
# Note: rolling_3d_sales includes current day + previous 2 days (ROWS BETWEEN 2 PRECEDING AND CURRENT ROW).
CHALLENGE_2_SQL = """
-- Write your SQL query below:
SELECT
    sale_date,
    amount,
    SUM(amount) OVER (ORDER BY sale_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_sales,
    SUM(amount) OVER (ORDER BY sale_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS rolling_3d_sales
FROM daily_sales
ORDER BY sale_date;
"""


# Challenge 3: Deduplication with ROW_NUMBER
# Get only the latest updated record for each event_id.
# Columns: event_id, user_id, action, updated_at
CHALLENGE_3_SQL = """
-- Write your SQL query below:
WITH ranked_events AS (
    SELECT
        event_id,
        user_id,
        action,
        updated_at,
        ROW_NUMBER() OVER (PARTITION BY event_id ORDER BY updated_at DESC) AS rn
    FROM event_logs
)
SELECT
    event_id,
    user_id,
    action,
    updated_at
FROM ranked_events
WHERE rn = 1
ORDER BY event_id;
"""


# Challenge 4: Consecutive login streak (Gaps & Islands problem)
# Find all users who logged in for at least 3 consecutive days.
# Columns: user_id
CHALLENGE_4_SQL = """
-- Write your SQL query below:
WITH ranked AS (
    SELECT
        user_id,
        login_date,
        -- Subtract row number of days from date: consecutive dates will result in the same base date
        date(login_date, '-' || (ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date)) || ' days') AS grp
    FROM (
        SELECT DISTINCT user_id, login_date FROM user_logins
    ) u
)
SELECT
    user_id
FROM ranked
GROUP BY user_id, grp
HAVING COUNT(*) >= 3
ORDER BY user_id;
"""


# Challenge 5: Month-over-month / Day-over-day growth using LAG
# Compare daily amount with previous day's amount and calculate difference.
# Columns: sale_date, amount, prev_day_amount, diff
CHALLENGE_5_SQL = """
-- Write your SQL query below:
SELECT
    sale_date,
    amount,
    LAG(amount) OVER (ORDER BY sale_date) AS prev_day_amount,
    amount - LAG(amount) OVER (ORDER BY sale_date) AS diff
FROM daily_sales
ORDER BY sale_date;
"""


# =========================================================================
# Tests
# =========================================================================

def test_challenge_1_dense_rank():
    conn = get_connection()
    results = run_query(conn, CHALLENGE_1_SQL)
    # Engineering: Alice(120k, r=1), Bob(120k, r=1), Charlie(95k, r=2)
    # Marketing: Hannah(95k, r=1), Ian(85k, r=2)
    # Sales: Evan(110k, r=1), Fiona(110k, r=1), George(90k, r=2)
    expected = [
        ("Engineering", "Charlie", 95000, 2),
        ("Marketing", "Ian", 85000, 2),
        ("Sales", "George", 90000, 2),
    ]
    assert results == expected, f"Got: {results}"


def test_challenge_2_rolling_and_cumulative():
    conn = get_connection()
    results = run_query(conn, CHALLENGE_2_SQL)
    # row 0: 100 -> cum: 100, roll3: 100
    # row 1: 150 -> cum: 250, roll3: 250
    # row 2: 200 -> cum: 450, roll3: 450
    # row 3: 120 -> cum: 570, roll3: 150+200+120 = 470
    assert results[0] == ("2026-01-01", 100, 100, 100)
    assert results[1] == ("2026-01-02", 150, 250, 250)
    assert results[2] == ("2026-01-03", 200, 450, 450)
    assert results[3] == ("2026-01-04", 120, 570, 470)


def test_challenge_3_dedup_latest_event():
    conn = get_connection()
    results = run_query(conn, CHALLENGE_3_SQL)
    expected = [
        (101, 1, "view", "2026-01-01 10:05:00"),
        (102, 2, "click", "2026-01-01 11:00:00"),
        (103, 1, "purchase", "2026-01-01 12:02:00"),
    ]
    assert results == expected


def test_challenge_4_consecutive_logins():
    conn = get_connection()
    results = run_query(conn, CHALLENGE_4_SQL)
    # User 1 logged in on 01-01, 01-02, 01-03 (3 consecutive)
    # User 2 logged in on 01-01, 01-03 (not consecutive)
    # User 3 logged in on 01-02, 01-03, 01-04 (3 consecutive)
    assert results == [(1,), (3,)]


def test_challenge_5_lag_diff():
    conn = get_connection()
    results = run_query(conn, CHALLENGE_5_SQL)
    assert results[0] == ("2026-01-01", 100, None, None)
    assert results[1] == ("2026-01-02", 150, 100, 50)
    assert results[2] == ("2026-01-03", 200, 150, 50)
    assert results[3] == ("2026-01-04", 120, 200, -80)
