# duration_calculator.py
import datetime as dt

def days_until_today(user_date: str) -> int:
    """
    Calculate how many days ago the given date was from today.
    Input format: YYYY-MM-DD
    """
    try:
        input_date = dt.datetime.strptime(user_date, "%Y-%m-%d").date()
        today = dt.date.today()
        delta = today - input_date
        return delta.days
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD.")

if __name__ == "__main__":
    date_input = input("Enter a date (YYYY-MM-DD): ")
    days = days_until_today(date_input)
    print(f"{date_input} was {days} days ago.")