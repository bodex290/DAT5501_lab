# duration_calculator.py
import datetime as dt

DATE_FMT = "%Y-%m-%d"

def _parse_date(date_str: str) -> dt.date:
    """
    Parse a YYYY-MM-DD string to a date.
    Raises ValueError if the format/content is invalid.
    """
    try:
        return dt.datetime.strptime(date_str, DATE_FMT).date()
    except ValueError as e:
        raise ValueError("Date must be in YYYY-MM-DD format") from e

def days_until_today(date_str: str) -> int:
    """
    Return the number of days from `date_str` to today.
    Positive for past dates, 0 for today, negative for future dates.
    """
    target = _parse_date(date_str)
    today = dt.date.today()
    return (today - target).days

if __name__ == "__main__":
    input_date = input("Enter a date (YYYY-MM-DD): ")
    try:
        days_diff = days_until_today(input_date)
        print(f"Days until today: {days_diff}")
    except ValueError as e:
        print(f"Error: {e}")