# test_duration_calculator.py
import unittest
from duration_calculator import days_until_today
import datetime as dt

class TestDurationCalculator(unittest.TestCase):

    def test_past_date(self):
        today = dt.date.today()
        past_date = today - dt.timedelta(days=10)
        self.assertEqual(days_until_today(str(past_date)), 10)

    def test_today_date(self):
        today = dt.date.today()
        self.assertEqual(days_until_today(str(today)), 0)

    def test_future_date(self):
        today = dt.date.today()
        future_date = today + dt.timedelta(days=5)
        self.assertEqual(days_until_today(str(future_date)), -5)

    def test_invalid_format(self):
        with self.assertRaises(ValueError):
            days_until_today("20/10/2025")

if __name__ == '__main__':
    unittest.main()