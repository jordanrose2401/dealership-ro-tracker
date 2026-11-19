"""
Tests for check_staleness() in app.py.

Every test uses fixed dates, so the results never depend on the clock.
Run from the project root with:  python -m unittest
"""

import unittest
from datetime import date

from app import STALE_AFTER_DAYS, check_staleness


# A fixed "today" used by the tests below.
TODAY = date(2026, 11, 18)


class CheckStalenessTests(unittest.TestCase):

    def test_opened_today_is_0_days_and_ok(self):
        self.assertEqual(check_staleness(date(2026, 11, 18), TODAY), (0, False))

    def test_6_days_is_ok(self):
        self.assertEqual(check_staleness(date(2026, 11, 12), TODAY), (6, False))

    def test_exactly_7_days_is_still_ok(self):
        # 7 is the limit; an order must be open MORE than 7 days to be stale.
        self.assertEqual(check_staleness(date(2026, 11, 11), TODAY), (7, False))

    def test_8_days_is_stale(self):
        self.assertEqual(check_staleness(date(2026, 11, 10), TODAY), (8, True))

    def test_counts_days_across_a_month_end(self):
        # November 28 to December 6 is 8 calendar days.
        self.assertEqual(check_staleness(date(2026, 11, 28), date(2026, 12, 6)), (8, True))

    def test_stale_limit_is_7_days(self):
        self.assertEqual(STALE_AFTER_DAYS, 7)


if __name__ == "__main__":
    unittest.main()
