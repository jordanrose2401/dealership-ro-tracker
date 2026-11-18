"""
load_orders.py - loads repair orders from a CSV file into data/orders.db.

How to run it (from the project root), either of these works:
    python scripts\\load_orders.py data\\good_orders.csv
    python scripts\\load_orders.py good_orders.csv     (looks in the data folder)

What it does:
  1. Finds the CSV file and checks its header row.
     If the file is missing or the headers are wrong, it stops right away
     and the database is not touched.
  2. Checks every row against the rules. Good rows are kept,
     bad rows are rejected with a reason.
  3. Rebuilds the database in ONE transaction: either the whole rebuild
     succeeds, or nothing changes and the old database stays as it was.
  4. Prints a summary of what was loaded and what was rejected.
     Full VINs are never printed.
"""

import argparse
import csv
import sqlite3
from datetime import date, datetime
from pathlib import Path


# ---------------------------------------------------------------------
# Settings - change things here, not further down
# ---------------------------------------------------------------------

# The only reasons allowed for an open order. This is the ONE place they are listed.
REASONS = ["Parts", "Customer Approval", "Technician", "Warranty"]

# The six column names the CSV must have (in any order).
EXPECTED_HEADERS = ["order_no", "date_opened", "date_completed", "make_model", "vin", "reason"]

# Characters a VIN may use: digits and uppercase letters, but never I, O, or Q.
VIN_CHARACTERS = set("0123456789ABCDEFGHJKLMNPRSTUVWXYZ")
VIN_LENGTH = 17

# The data folder sits at the project root, next to the scripts folder.
# __file__ is this script, .parent is "scripts", .parent again is the project root.
DATA_FOLDER = Path(__file__).resolve().parent.parent / "data"
DATABASE_PATH = DATA_FOLDER / "orders.db"


# ---------------------------------------------------------------------
# Database table design
# The database double-checks what it can on its own: required columns,
# a unique order number, the order number range, the reason list, and
# the open/completed rules.
# ---------------------------------------------------------------------

CREATE_REASONS_TABLE = """
CREATE TABLE reasons (
    name TEXT PRIMARY KEY
)
"""

CREATE_ORDERS_TABLE = """
CREATE TABLE orders (
    order_no       INTEGER NOT NULL UNIQUE
                   CHECK (order_no BETWEEN 10000 AND 99999),
    date_opened    TEXT NOT NULL,
    date_completed TEXT,
    make_model     TEXT NOT NULL CHECK (make_model <> ''),
    vin_last4      TEXT NOT NULL CHECK (length(vin_last4) = 4),
    reason         TEXT REFERENCES reasons(name),
    CHECK ((date_completed IS NULL     AND reason IS NOT NULL) OR
           (date_completed IS NOT NULL AND reason IS NULL)),
    CHECK (date_completed IS NULL OR date_completed >= date_opened)
)
"""


# ---------------------------------------------------------------------
# Step 1: find and read the CSV file
# ---------------------------------------------------------------------

def find_csv(path_text):
    """Find the CSV file. If just a file name was given, also look in the data folder."""
    typed_path = Path(path_text)
    if typed_path.is_file():
        return typed_path

    # Only a bare file name (like "good_orders.csv") gets a second look in data\.
    if len(typed_path.parts) == 1:
        data_path = DATA_FOLDER / typed_path.name
        if data_path.is_file():
            return data_path

    raise SystemExit(
        f"File not found: {path_text}\n"
        f"Nothing was loaded and the database was not changed."
    )


def read_csv(csv_path):
    """Read the header names and all the rows from the CSV file."""
    # "utf-8-sig" quietly removes the invisible marker Excel sometimes adds
    # at the very start of a file, so the first header reads as "order_no".
    try:
        with open(csv_path, newline="", encoding="utf-8-sig") as csv_file:
            reader = csv.DictReader(csv_file)
            headers = reader.fieldnames
            rows = list(reader)
    except (UnicodeDecodeError, csv.Error) as problem:
        raise SystemExit(
            f"Could not read {csv_path}: {problem}\n"
            f"Nothing was loaded and the database was not changed."
        )
    return headers, rows


def check_headers(headers, csv_path):
    """Stop the whole load if the header row isn't exactly the six expected names."""
    if not headers:
        raise SystemExit(
            f"{csv_path} is empty or has no header row.\n"
            f"Nothing was loaded and the database was not changed."
        )

    missing = [name for name in EXPECTED_HEADERS if name not in headers]
    unexpected = [name for name in headers if name not in EXPECTED_HEADERS]
    repeated = sorted({name for name in headers if headers.count(name) > 1})

    if missing or unexpected or repeated:
        problems = []
        if missing:
            problems.append("missing: " + ", ".join(missing))
        if unexpected:
            problems.append("unexpected: " + ", ".join(str(name) for name in unexpected))
        if repeated:
            problems.append("repeated: " + ", ".join(repeated))
        raise SystemExit(
            f"Wrong headers in {csv_path} ({'; '.join(problems)}).\n"
            f"Expected exactly: {', '.join(EXPECTED_HEADERS)}\n"
            f"Nothing was loaded and the database was not changed."
        )


# ---------------------------------------------------------------------
# Step 2: check each row
# Each check function returns an error message, or None if all is well.
# ---------------------------------------------------------------------

def get_cell(row, column):
    """Get a cell's text. A cell missing from a short row comes back as blank text."""
    value = row.get(column)
    if value is None:
        return ""
    return value


def check_order_no(text):
    """order_no must be a 5-digit whole number from 10000 to 99999."""
    if len(text) == 5 and text.isascii() and text.isdigit() and int(text) >= 10000:
        return None
    return f"order_no '{text}' must be a whole number from 10000 to 99999"


def parse_date(text):
    """Turn YYYY-MM-DD text into a date. Returns None if it isn't a real date in that exact format."""
    try:
        the_date = datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        return None
    # Make sure it was written exactly as YYYY-MM-DD (for example, not 2026-1-5).
    if the_date.isoformat() != text:
        return None
    return the_date


def check_date(text, column, today):
    """A date must be a real YYYY-MM-DD date and not in the future."""
    the_date = parse_date(text)
    if the_date is None:
        return f"{column} '{text}' is not a real YYYY-MM-DD date"
    if the_date > today:
        return f"{column} {text} is in the future"
    return None


def check_reason(reason, is_completed):
    """Open orders need a reason from the list. Completed orders need a blank reason."""
    if is_completed:
        if reason != "":
            return "completed order must have a blank reason"
        return None
    if reason == "":
        return "open order must have a reason"
    if reason not in REASONS:
        return f"reason '{reason}' is not one of: {', '.join(REASONS)}"
    return None


def check_vin(vin):
    """A VIN must be 17 uppercase letters/digits with no I, O, or Q."""
    if len(vin) == VIN_LENGTH and all(character in VIN_CHARACTERS for character in vin):
        return None
    # The VIN itself is never put in the message, so it can't be printed.
    return "vin is not valid (must be 17 uppercase letters/digits, no I, O, or Q)"


def check_row(row, today):
    """Check one row against every rule. Returns a list of error messages (empty = valid)."""
    errors = []

    # A short row: the CSV reader fills the missing cells with None.
    if None in row.values():
        errors.append("row has missing cells")
    # A long row: the CSV reader puts the extra cells under the key None.
    if None in row:
        errors.append("row has extra cells")

    order_no = get_cell(row, "order_no")
    opened = get_cell(row, "date_opened")
    completed = get_cell(row, "date_completed")
    make_model = get_cell(row, "make_model")
    vin = get_cell(row, "vin")
    reason = get_cell(row, "reason")

    errors.append(check_order_no(order_no))

    if opened == "":
        errors.append("date_opened is required")
    else:
        errors.append(check_date(opened, "date_opened", today))

    if completed != "":
        errors.append(check_date(completed, "date_completed", today))
        # Only compare the two dates when both are real dates.
        opened_date = parse_date(opened)
        completed_date = parse_date(completed)
        if opened_date and completed_date and completed_date < opened_date:
            errors.append(f"date_completed {completed} is before date_opened {opened}")

    errors.append(check_reason(reason, is_completed=(completed != "")))

    if make_model.strip() == "":
        errors.append("make_model is required")

    errors.append(check_vin(vin))

    # Throw away the "None" results (the checks that passed).
    return [error for error in errors if error is not None]


def make_order(row):
    """Turn a valid row into the values stored in the database."""
    completed = get_cell(row, "date_completed")
    reason = get_cell(row, "reason")
    return {
        "order_no": int(get_cell(row, "order_no")),
        "date_opened": get_cell(row, "date_opened"),
        "date_completed": completed if completed != "" else None,  # None becomes SQL NULL
        "make_model": get_cell(row, "make_model"),
        "vin_last4": get_cell(row, "vin")[-4:],  # only the last 4 characters are stored
        "reason": reason if reason != "" else None,  # None becomes SQL NULL
    }


def sort_rows(rows, today):
    """Split the rows into loaded orders and rejected rows."""
    loaded = []    # list of (row number, order)
    rejected = []  # list of (row number, order number text, error messages)
    first_seen = {}  # order number -> row number where it was first loaded

    for row_number, row in enumerate(rows, start=1):
        errors = check_row(row, today)

        # The duplicate check runs last, and only on rows that passed everything
        # else, so only a fully valid row can count as the "first" one.
        if not errors:
            order = make_order(row)
            if order["order_no"] in first_seen:
                earlier_row = first_seen[order["order_no"]]
                errors.append(
                    f"duplicate order_no {order['order_no']} (already loaded from row {earlier_row})"
                )
            else:
                first_seen[order["order_no"]] = row_number
                loaded.append((row_number, order))

        if errors:
            rejected.append((row_number, get_cell(row, "order_no"), errors))

    return loaded, rejected


# ---------------------------------------------------------------------
# Step 3: rebuild the database in one transaction
# ---------------------------------------------------------------------

def create_tables(connection):
    """Delete the old tables and make fresh ones."""
    # Drop orders first, because it points at the reasons table.
    connection.execute("DROP TABLE IF EXISTS orders")
    connection.execute("DROP TABLE IF EXISTS reasons")
    connection.execute(CREATE_REASONS_TABLE)
    # Fill the reasons table from the REASONS list, using ? placeholders.
    connection.executemany(
        "INSERT INTO reasons (name) VALUES (?)",
        [(reason,) for reason in REASONS],
    )
    connection.execute(CREATE_ORDERS_TABLE)


def insert_orders(connection, loaded):
    """Add the valid orders to the database, using ? placeholders."""
    connection.executemany(
        "INSERT INTO orders "
        "(order_no, date_opened, date_completed, make_model, vin_last4, reason) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        [
            (
                order["order_no"],
                order["date_opened"],
                order["date_completed"],
                order["make_model"],
                order["vin_last4"],
                order["reason"],
            )
            for _, order in loaded
        ],
    )


def rebuild_database(loaded):
    """Rebuild the database as one all-or-nothing transaction."""
    DATA_FOLDER.mkdir(exist_ok=True)

    # isolation_level=None means Python won't start or end transactions on
    # its own, so the BEGIN and COMMIT below are fully in our control.
    connection = sqlite3.connect(DATABASE_PATH, isolation_level=None)
    try:
        # Turn on the check that reasons must come from the reasons table.
        # (This must be done before BEGIN; SQLite ignores it inside a transaction.)
        connection.execute("PRAGMA foreign_keys = ON")

        connection.execute("BEGIN")
        create_tables(connection)
        insert_orders(connection, loaded)
        connection.execute("COMMIT")  # only now do the changes become permanent
    except sqlite3.Error as problem:
        # Something went wrong: undo everything since BEGIN.
        if connection.in_transaction:
            connection.execute("ROLLBACK")
        raise SystemExit(
            f"Database error: {problem}\n"
            f"Nothing was saved; the old database was left as it was."
        )
    finally:
        connection.close()


# ---------------------------------------------------------------------
# Step 4: print the summary
# ---------------------------------------------------------------------

def print_summary(csv_path, today, loaded, rejected):
    """Print how many rows were loaded and rejected, and why. No VINs are printed."""
    print(f"Loading {csv_path}  (today is {today.isoformat()})")

    loaded_numbers = ", ".join(str(row_number) for row_number, _ in loaded) or "none"
    print(f"Rows loaded:   {len(loaded)}  (rows: {loaded_numbers})")

    print(f"Rows rejected: {len(rejected)}")
    for row_number, order_no, errors in rejected:
        label = f"Row {row_number}"
        if order_no:
            label += f" (order {order_no})"
        print(f"  {label}: {'; '.join(errors)}")

    print(f"Database written to {DATABASE_PATH}")


# ---------------------------------------------------------------------
# Main - runs everything in order
# ---------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Load repair orders from a CSV into data/orders.db.")
    parser.add_argument("csv_path", help="the CSV file to load, e.g. data\\good_orders.csv")
    arguments = parser.parse_args()

    # Read today's date from the computer's clock.
    today = date.today()

    # Steps 1-2 never touch the database, so a bad file leaves it unchanged.
    csv_path = find_csv(arguments.csv_path)
    headers, rows = read_csv(csv_path)
    check_headers(headers, csv_path)
    loaded, rejected = sort_rows(rows, today)

    # Step 3: rebuild the database (all or nothing).
    rebuild_database(loaded)

    # Step 4: report what happened.
    print_summary(csv_path, today, loaded, rejected)


# Only run main() when this file is run directly (not when imported).
if __name__ == "__main__":
    main()
