# 🗓️ Calendar Printer — DAT5501 Portfolio Activity

## 📁 File Directory
```
CalendarPrinter/
├── calendar_printer.py              # Main script — prints a formatted monthly calendar
├── test_print_calendar_unittest.py  # Unit tests for validating output formatting
└── README.md                        # This file — project documentation
```

---

## 🧠 Overview

This activity demonstrates how to build a simple yet structured Python program that prints a calendar layout based on user input for the number of days in a month and the starting day of the week.

It also includes **comprehensive unit testing** using the `unittest` module to verify that the program’s output matches expected alignment and formatting.

This exercise focuses on writing **clear, maintainable, and testable code**, aligning with the professional software development practices emphasised in the **DAT5501: Analysis, Software and Career Practice** module.

---

## ⚙️ How It Works

1. The user is prompted to enter:
   - Number of days in the month (`days`)
   - Starting day of the week (`start`, where `0 = Sun`, `6 = Sat`)

2. The program:
   - Prints the day headers (`Sun Mon Tue Wed Thu Fri Sat`)
   - Aligns each day correctly under its weekday column
   - Starts a new line after every Saturday

3. The output visually represents a monthly calendar grid.

---

## 🧪 Testing

The file `test_print_calendar_unittest.py` includes:

- **Golden-path tests** verifying output for multiple `days` and `start` combinations  
- **Header and alignment checks** to ensure day placement accuracy  
- **Trailing newline validation** for consistent print formatting  

Each test compares the captured output to a dynamically generated expected result, ensuring robust verification of both logic and formatting.

To run all tests, use:

```bash
python -m unittest test_print_calendar_unittest.py
```

## 🧩 Learning Outcomes

This activity builds on the following Knowledge, Skills, and Behaviours (KSBs) from the apprenticeship standard.

🧠 Knowledge
	•	K53 – Understanding barriers to effective data communication between analysts and stakeholders by producing clear, readable console outputs.
	•	K54 – Interpreting structured textual data and verifying alignment logic through systematic testing.
	•	K57 – Applying good data handling and structured output formatting practices, foundational to later analytical workflows.

## 🧰 Skills
	•	S49 – Applying analytical and logical reasoning to generate structured program outputs.
	•	S50 – Communicating information clearly through formatted console output and documented test cases.
	•	S53 – Using confirmatory testing (unit tests) to validate output accuracy and program stability.
	•	S55 – Employing Python as an industry-standard tool for structured problem solving and testing automation.

## 💼 Behaviours
	•	B3 (Professionalism & Quality) – Maintaining high code quality through consistent formatting, documentation, and version control.
	•	B6 (Continuous Learning) – Using testing and refactoring to iteratively improve the reliability of the solution.

## 💡 Reflection on Learning

Through this activity, I improved my ability to:
	•	Write modular and testable Python code that adheres to professional standards.
	•	Develop automated test cases that confirm output accuracy and formatting.
	•	Apply structured problem-solving by combining logic, formatting, and validation.
	•	Use GitHub version control to commit and track incremental improvements.

This reinforced the importance of clarity, testing, and documentation — all essential components of professional software development within data analysis projects.
