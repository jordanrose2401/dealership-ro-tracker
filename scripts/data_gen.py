"""
data_gen.py - makes sample repair order data for the RO tracker.

It writes two files into the data folder (next to the scripts folder):
  - good_orders.csv : 12 valid orders
  - bad_orders.csv  : 6 orders that each break exactly one rule

Dates are always worked out from today's date, so the ages of the
orders stay the same no matter which day you run it. Everything else
(order numbers, makes/models, VINs) comes from a fixed random seed,
so running it twice on the same day gives identical files.

Run it with:  python scripts/data_gen.py
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path


# ---------------------------------------------------------------------
# Settings - change things here, not further down
# ---------------------------------------------------------------------

# The fixed seed. Same seed = same order numbers, cars, and VINs every run.
SEED = 2026

# The only reasons allowed for an open order. A completed order has no reason.
REASONS = ["Parts", "Customer Approval", "Technician", "Warranty"]

# Cars to pick from. Make and model are kept together in one column.
MAKE_MODELS = [
    "Ford F-150",
    "Toyota Camry",
    "Honda Civic",
    "Chevrolet Silverado",
    "Nissan Altima",
    "Jeep Wrangler",
    "Subaru Outback",
    "Hyundai Tucson",
    "Kia Sorento",
    "Ram 1500",
]

# Letters and numbers a VIN may use. Real VINs never use I, O, or Q.
VIN_CHARACTERS = "0123456789ABCDEFGHJKLMNPRSTUVWXYZ"
VIN_LENGTH = 17

# Column headers, in order, for both CSV files.
HEADERS = ["order_no", "date_opened", "date_completed", "make_model", "vin", "reason"]

# Where the CSV files go: the "data" folder at the project root.
# __file__ is this script, .parent is "scripts", .parent again is the project root.
DATA_FOLDER = Path(__file__).resolve().parent.parent / "data"


# ---------------------------------------------------------------------
# Row plans - what each row should look like
#
#   opened    = how many days ago the order was opened (None = leave blank)
#   completed = how many days ago it was completed (None = still open)
#   reason    = the delay reason ("" = leave blank)
#   covers    = which test case(s) the row covers (only printed, never saved)
# ---------------------------------------------------------------------

GOOD_PLANS = [
    {"opened": 0,  "completed": None, "reason": "Parts",
     "covers": "Opened today; reason Parts"},
    {"opened": 6,  "completed": None, "reason": "Customer Approval",
     "covers": "Opened 6 days ago (not stale); reason Customer Approval"},
    {"opened": 7,  "completed": None, "reason": "Technician",
     "covers": "Opened exactly 7 days ago (not stale); reason Technician"},
    {"opened": 8,  "completed": None, "reason": "Warranty",
     "covers": "Opened 8 days ago (stale); reason Warranty"},
    {"opened": 2,  "completed": None, "reason": "Parts",
     "covers": "Filler"},
    {"opened": 12, "completed": None, "reason": "Customer Approval",
     "covers": "Filler (stale)"},
    {"opened": 21, "completed": None, "reason": "Technician",
     "covers": "Filler (stale, oldest)"},
    {"opened": 1,  "completed": None, "reason": "Warranty",
     "covers": "Filler"},
    {"opened": 15, "completed": None, "reason": "Parts",
     "covers": "Filler (stale)"},
    {"opened": 10, "completed": 2,    "reason": "",
     "covers": "Completed order with a completion date and blank reason"},
    {"opened": 5,  "completed": 0,    "reason": "",
     "covers": "Completed order (completed today)"},
    {"opened": 4,  "completed": 4,    "reason": "",
     "covers": "Completed order (completed the same day it opened)"},
]

BAD_PLANS = [
    {"opened": 3,    "completed": None, "reason": "Backorder",
     "covers": "Reason is not on the list"},
    {"opened": None, "completed": None, "reason": "Parts",
     "covers": "Missing opening date"},
    {"opened": 5,    "completed": None, "reason": "",
     "covers": "Open order with a blank reason"},
    {"opened": 4,    "completed": 6,    "reason": "",
     "covers": "Completion date earlier than opening date"},
    {"opened": 2,    "completed": None, "reason": "Technician",
     "covers": "Duplicate order number (first of the pair)"},
    {"opened": 9,    "completed": None, "reason": "Warranty",
     "covers": "Duplicate order number (same as the row above)"},
]


# ---------------------------------------------------------------------
# Small helper functions
# ---------------------------------------------------------------------

def days_ago_to_date_text(today, days_ago):
    """Turn 'N days ago' into a YYYY-MM-DD date. None gives a blank cell."""
    if days_ago is None:
        return ""
    the_date = today - timedelta(days=days_ago)
    return the_date.isoformat()


def make_vin(rng, used_vins):
    """Make a new 17-character VIN that hasn't been used yet."""
    while True:
        vin = "".join(rng.choice(VIN_CHARACTERS) for _ in range(VIN_LENGTH))
        if vin not in used_vins:
            used_vins.add(vin)
            return vin


def build_rows(plans, order_numbers, rng, used_vins, today):
    """Turn a list of row plans into finished rows ready for the CSV."""
    rows = []
    for plan, order_no in zip(plans, order_numbers):
        row = {
            "order_no": order_no,
            "date_opened": days_ago_to_date_text(today, plan["opened"]),
            "date_completed": days_ago_to_date_text(today, plan["completed"]),
            "make_model": rng.choice(MAKE_MODELS),
            "vin": make_vin(rng, used_vins),
            "reason": plan["reason"],
        }
        rows.append(row)
    return rows


def write_csv(file_path, rows):
    """Write the rows to a CSV file, replacing the old file if there is one."""
    with open(file_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)


def print_summary(file_name, rows, plans):
    """Print each row's order number and the test case(s) it covers."""
    print()
    print(f"{file_name} ({len(rows)} rows)")
    for row_number, (row, plan) in enumerate(zip(rows, plans), start=1):
        print(f"  Row {row_number:>2}  order {row['order_no']}  ->  {plan['covers']}")


# ---------------------------------------------------------------------
# Main - runs everything in order
# ---------------------------------------------------------------------

def main():
    # Read today's date from the computer's clock.
    today = date.today()

    # Start the random number generator with the fixed seed.
    rng = random.Random(SEED)

    # Pick 17 different order numbers: 12 for the good file, 5 for the bad file.
    order_numbers = rng.sample(range(10000, 100000), 17)
    good_numbers = order_numbers[:12]
    bad_numbers = order_numbers[12:]

    # The 6th bad row reuses the 5th bad row's number (the duplicate case).
    bad_numbers.append(bad_numbers[4])

    # Keep track of every VIN so none repeat, even across the two files.
    used_vins = set()

    good_rows = build_rows(GOOD_PLANS, good_numbers, rng, used_vins, today)
    bad_rows = build_rows(BAD_PLANS, bad_numbers, rng, used_vins, today)

    # Make the data folder if it doesn't exist yet, then save both files.
    DATA_FOLDER.mkdir(exist_ok=True)
    write_csv(DATA_FOLDER / "good_orders.csv", good_rows)
    write_csv(DATA_FOLDER / "bad_orders.csv", bad_rows)

    print(f"Sample data written to {DATA_FOLDER} (today is {today.isoformat()})")
    print_summary("good_orders.csv", good_rows, GOOD_PLANS)
    print_summary("bad_orders.csv", bad_rows, BAD_PLANS)


# Only run main() when this file is run directly (not when imported).
if __name__ == "__main__":
    main()
