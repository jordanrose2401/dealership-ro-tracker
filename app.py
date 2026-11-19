"""
app.py - the Repair Order Board.

Shows every OPEN repair order (no completion date) from data/orders.db,
with how many days it has been open and whether it is STALE or OK.

How to start it (from the project root):
    python app.py
Then open http://127.0.0.1:5000 in a browser.

Importing this file (as the tests do) does NOT start the server or open
the database. Both only happen when the page is visited or the file is run.
"""

import sqlite3
from datetime import date
from pathlib import Path

from flask import Flask, render_template


# ---------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------

# An order is stale once it has been open MORE than this many calendar days.
STALE_AFTER_DAYS = 7

# The database sits in the data folder next to this file.
DATABASE_PATH = Path(__file__).resolve().parent / "data" / "orders.db"

# Plain messages shown on the page instead of the table.
NO_DATA_MESSAGE = "No data loaded, run the loader."
NO_OPEN_ORDERS_MESSAGE = "No open orders to display."
ERROR_MESSAGE = "Something went wrong reading the orders. Try running the loader again."

# Open orders only (no completion date), oldest opened first.
# The oldest date has the most days open, so the stalest orders come out on top.
OPEN_ORDERS_QUERY = """
SELECT order_no, date_opened, make_model, vin_last4, reason
FROM orders
WHERE date_completed IS NULL
ORDER BY date_opened ASC, order_no ASC
"""

app = Flask(__name__)


# ---------------------------------------------------------------------
# Dates and staleness
# ---------------------------------------------------------------------

def get_today():
    """Today's date. This is the ONLY place in the app that reads the clock."""
    return date.today()


def check_staleness(date_opened, today):
    """Given two dates, return (days open, is it stale?). Never reads the clock."""
    days_open = (today - date_opened).days  # counts every calendar day
    is_stale = days_open > STALE_AFTER_DAYS
    return days_open, is_stale


def format_as_of(today):
    """Turn a date into text like 'November 18, 2026' (no leading zero on the day)."""
    return f"{today.strftime('%B')} {today.day}, {today.year}"


# ---------------------------------------------------------------------
# Reading the database
# ---------------------------------------------------------------------

def read_open_orders():
    """Read the open orders from the database, opened in read-only mode."""
    # "mode=ro" means read-only: SQLite will not write to the file,
    # and it will NOT create an empty database if the file is missing.
    database_uri = DATABASE_PATH.as_uri() + "?mode=ro"
    connection = sqlite3.connect(database_uri, uri=True)
    try:
        return connection.execute(OPEN_ORDERS_QUERY).fetchall()
    finally:
        connection.close()  # always close, even if the query fails


def build_board_rows(database_rows, today):
    """Turn database rows into rows for the page, adding days open and stale."""
    board_rows = []
    for order_no, date_opened_text, make_model, vin_last4, reason in database_rows:
        # The database stores dates as ISO text; turn it into a real date first.
        date_opened = date.fromisoformat(date_opened_text)
        days_open, is_stale = check_staleness(date_opened, today)
        board_rows.append({
            "order_no": order_no,
            "days_open": days_open,
            "make_model": make_model,
            "vin_last4": vin_last4,
            "reason": reason,
            "is_stale": is_stale,
        })
    return board_rows


# ---------------------------------------------------------------------
# The web page
# ---------------------------------------------------------------------

def show_message(as_of, message):
    """Show the page with a plain message instead of the table."""
    return render_template("board.html", as_of=as_of, message=message)


@app.route("/")
def board():
    """The one and only page: the board of open repair orders."""
    today = get_today()
    as_of = format_as_of(today)

    # Check the file exists BEFORE connecting, so a missing database is never created.
    if not DATABASE_PATH.is_file():
        return show_message(as_of, NO_DATA_MESSAGE)

    try:
        orders = build_board_rows(read_open_orders(), today)
    except Exception:
        # Print the real error (with details) in the terminal running the server,
        # but show only a plain message on the page.
        app.logger.exception("Could not read the orders from %s", DATABASE_PATH)
        return show_message(as_of, ERROR_MESSAGE), 500

    if not orders:
        return show_message(as_of, NO_OPEN_ORDERS_MESSAGE)

    stale_count = sum(1 for order in orders if order["is_stale"])
    return render_template(
        "board.html",
        as_of=as_of,
        orders=orders,
        stale_count=stale_count,
        message=None,
    )


# ---------------------------------------------------------------------
# Start the server - only when this file is run directly
# ---------------------------------------------------------------------

if __name__ == "__main__":
    # Stated on purpose: only this computer can reach it, and debug mode is off.
    app.run(host="127.0.0.1", port=5000, debug=False)
