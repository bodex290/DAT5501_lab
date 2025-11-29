# DAT5501 Portfolio – Analysis, Software and Career Practice

### **Student:** Samuel Ojeiwa  
### **Module Code:** DAT5501  
### **Assessment:** 001 – Portfolio (50%)  
### **Deadline:** 29 November 2025, 23:59  

---

## 📘 Overview

This repository contains my **DAT5501 Portfolio** for *Analysis, Software and Career Practice*.  
It showcases my weekly coding activities, data analysis workflows, and applied technical exercises completed throughout the semester.  

Each sub-folder documents an individual activity, including well-commented source code, a clear commit history, a dedicated `README.md`, and unit tests where applicable.

> The portfolio demonstrates the development of **Knowledge, Skills, and Behaviours (KSBs)** required for a data analytics professional, focusing on reproducibility, testing, and clear communication of technical work.

---

## 🧩 Repository Structure
```
DAT5501_lab/
├── README.md                         ← (this file)
├── requirements.txt
└── DAT5501_lab/
├── AssetPrices/
│   ├── README.md
│   ├── asset_prices.py
│   └── test_asset_prices.py
│
├── CalendarPrinter/
│   ├── README.md
│   ├── calendar_printer.py
│   └── test_calendar_printer_unittest.py
│
├── DurationCalculator/
│   ├── README.md
│   ├── duration_calculator.py
│   ├── duration_from_csv.py
│   ├── test_duration_calculator.py
│   ├── random_dates_fixed.csv
│   └── fix_csv.py
│
├── PolynomialModelComparison/
│   ├── README.md
│   ├── polynomial_models.py
│   └── test_polynomial_models.py
│
├── USelection/
│   ├── README.md
│   ├── us_election.py
│   └── test_us_election.py
│
├── RuleOfLawMap/
│   └── README.md
│
└── DataPipelineCI/
└── README.md
```
---

## 🧠 Learning Focus

Each activity contributes to the development of professional KSBs defined in the module brief:

| Category | KSB | Description |
|-----------|-----|-------------|
| **Knowledge** | K53 | Barriers to effective data analysis and stakeholder communication |
| | K54 | Interpreting and evaluating complex information from diverse datasets |
| | K57 | Data processing, storage, and analytical decision-making |
| | K59 | Applying analytics to improve business operations |
| | K60 | Ethical and legal considerations in data analytics |
| **Skills** | S49 | Apply data analysis methods to drive improvement |
| | S50 | Present and communicate analysis outputs effectively |
| | S51 | Identify and overcome barriers to effective analysis |
| | S53 | Validate and test analysis results |
| | S55 | Analyse large datasets using industry-standard tools |

---

## 🧮 Key Activities


## 1) **Duration Calculator**  
📁 `DAT5501_lab/DurationCalculator`  
Calculates the number of days between a given date and today, with strict input validation and unit testing.  
Also includes a CSV-processing tool using NumPy day precision.

✔ Demonstrates **S49**, **S53**, **S50**

---

## 2) **Asset Prices Analysis (yfinance + pandas)**  
📁 `DAT5501_lab/AssetPrices`  
Downloads 1 year of historical data for a selected ticker, computes returns, plots price trends, and includes a fully tested `returns()` helper function.

✔ Demonstrates **K57**, **S49**, **S53**

---

## 3) **Calendar Printer (CLI Tool)**  
📁 `DAT5501_lab/CalendarPrinter`  
Prints a month layout given `days` (28–31) and `start` (Sun=0…Sat=6).  
Formatting matches unit tests exactly, including spacing, header, and trailing newline.

✔ Demonstrates **S53**, **S50** (format-sensitive testing)

---

## 4) **Polynomial Model Comparison**  
📁 `DAT5501_lab/PolynomialModelComparison`  
Fits polynomial models of varying orders and compares them using metrics such as SSE, RMSE, and BIC.  
Includes visualisation and interpretation of underfitting vs overfitting.

✔ Demonstrates **K54**, **S49**, **S53**

---

## 5) **US Election Voting Data Analysis**  
📁 `DAT5501_lab/USelection`  
Loads and analyses US election primary data.  
Includes:  
- Data cleaning  
- Histogram and bar-chart visualisation  
- Unit tests for loading, filtering, and validation

✔ Demonstrates **K54**, **S50**, **S55**

---

## 6) **World Rule of Law Map (Interactive Visualisation)**  
📁 `DAT5501_lab/RuleOfLawMap`  
Interactive choropleth visualising the Rule of Law Index based on OWID/WJP datasets.  
Includes year slider, preprocessing, and clear data-source documentation.

✔ Demonstrates **K54**, **S50**, **S55**

---

## 7) **Data Pipeline CI**  
📁 `DAT5501_lab/DataPipelineCI`  
A demonstration of a simple CI workflow for analytics code using unittest and automation principles.

✔ Demonstrates **S53**, **K57**

---

## ⚙️ Setup Instructions

1. Clone this repository:
   ```bash
   git clone https://github.com/bodex290/DAT5501_lab.git
   cd DAT5501_lab

2.	Create a virtual environment and install dependencies:
    ```bash
    python -m venv venv
    source venv/bin/activate       # macOS/Linux
    # venv\Scripts\activate        # Windows PowerShell
    pip install -r requirements.txt

3.	Run any activity module, for example:
    ```bash
    python DAT5501_lab/DurationCalculator/duration_calculator.py

4. Run all unit tests:
    ```bash
    python -m unittest discover
    

🧪 Testing & Validation

All activities include testing files following the unittest structure.
Continuous Integration (CI) setup can be extended via:
	•	CircleCI (.circleci/config.yml)
	•	GitHub Actions (.github/workflows/python-tests.yml)

Testing ensures:
	•	Functions return expected results.
	•	Error handling for invalid input.
	•	Data is parsed correctly before computation.

⸻

📄 Documentation & Professional Practice
	•	Each folder contains a local README.md documenting code logic, input formats, and expected outputs.
	•	Clear inline comments and docstrings for maintainability.
	•	Frequent commits with descriptive messages following a professional workflow.
	•	Code formatted according to PEP 8 style guidelines.

⸻

🧭 Reflection (for portfolio submission)

This portfolio demonstrates progressive development across multiple coding contexts.
Each project emphasises:
	•	Analytical thinking and validation.
	•	Professional documentation and reproducibility.
	•	Real-world data handling using Python, pandas, and NumPy.
	•	Ethical and legal awareness in data processing.
 
# 🧭 Brief Reflection

Working through these activities in small, focused iterations strengthened my ability to refactor code, test effectively, and communicate results clearly. Breaking tasks into steps made the code easier to maintain and gave me more confidence working with data, validation, and visualisation.

# ⚠️ Note on Branch Merging & CI

Some feature branches were not fully merged because CircleCI tests failed due to missing dependencies/configuration issues.
Although I attempted to resolve these, I was not able to stabilise the CI environment before submission.

Despite this, the repository still demonstrates a clear iterative workflow, structured commits, and consistent improvements in testing and code quality.
