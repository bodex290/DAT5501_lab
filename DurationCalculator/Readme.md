# Duration Calculator (DAT5501)

Calculate how many days a date is from today, validate the logic with unit tests, and extend the calculation to a list of dates loaded from a CSV. Built with Python, NumPy, and pandas.

Learning outcomes / KSBs (for portfolio reflection)
	•	S49: Apply data analysis (date parsing, differences)
	•	S50: Present results clearly (CLI output, tabular results)
	•	S53: Validate through unit tests (unittest)
	•	Repository skills: Frequent commits, clear structure, documentation

## Features

	•	days_until_today(user_date: str) → int
Returns the integer day difference from YYYY-MM-DD to today (negative for future).
	•	CLI script to read user input and print the result.
	•	CSV pipeline using NumPy daily precision (np.datetime64('today','D')) for stable diffs.
	•	Robust CSV support:
	•	Works with a clean header (date) and strict YYYY-MM-DD.
	•	Helper script to clean raw date lists (adds header, drops malformed rows).
	•	Unit tests for core logic and CSV processor.

## Repository Structure

DAT5501_lab/
└─ DAT5501_lab/
   └─ DurationCalculator/
      ├─ duration_calculator.py        # Base function + CLI input
      ├─ duration_from_csv.py          # CSV loader using NumPy daily diffs
      ├─ fix_csv.py                    # (Optional) cleans raw date lists -> headered CSV
      ├─ test_duration_calculator.py   # Unit tests for base function
      ├─ test_duration_from_csv.py     # Unit tests for CSV processor (optional)
      ├─ random_dates_fixed.csv        # Sample cleaned CSV (header: date)
      └─ README.md                     # This file


## Python packages

pandas
numpy
datetime



