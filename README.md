# DAT5501 Portfolio – Analysis, Software and Career Practice

### **Student:** Samuel Ojeiwa  
### **Module Code:** DAT5501  
### **Assessment:** 001 – Portfolio (50%)  
### **Deadline:** 20 November 2025, 23:59  

---

## 📘 Overview

This repository contains my **DAT5501 Portfolio** for *Analysis, Software and Career Practice*.  
It showcases my weekly coding activities, data analysis workflows, and applied technical exercises completed throughout the semester.  

Each sub-folder documents an individual activity, including well-commented source code, a clear commit history, a dedicated `README.md`, and unit tests where applicable.

> The portfolio demonstrates the development of **Knowledge, Skills, and Behaviours (KSBs)** required for a data analytics professional, focusing on reproducibility, testing, and clear communication of technical work.

---

## 🧩 Repository Structure

DAT5501_lab/
├── README.md                        ← (this file) overall portfolio overview
├── DAT5501_lab/
│   ├── DurationCalculator/           ← Activity 1: Date difference calculator
│   │   ├── README.md                 ← Detailed documentation for this activity
│   │   ├── duration_calculator.py
│   │   ├── duration_from_csv.py
│   │   ├── test_duration_calculator.py
│   │   ├── random_dates_fixed.csv
│   │   └── fix_csv.py
│   │
│   ├── RuleOfLawMap/                 ← Activity 2: Interactive world rule-of-law map (OWID)
│   │   └── README.md                 ← to be completed
│   │
│   ├── DataPipelineCI/               ← Activity 3: Continuous Integration pipeline
│   │   └── README.md
│   │
│   └── other_projects/…            ← Additional practicals or experiments
│
└── requirements.txt                  ← shared dependencies

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

### 1. [Duration Calculator](./DAT5501_lab/DurationCalculator/README.md)
A Python utility that:
- Calculates how many days a given date is from today.  
- Extends to multiple dates loaded from a CSV.  
- Includes unit tests, data cleaning, and NumPy-based day precision.  

> Demonstrates **S49**, **S50**, and **S53** through applied analysis and testing.

---

### 2. [World Rule of Law Map](./DAT5501_lab/RuleOfLawMap/README.md)
An interactive choropleth map visualising the **World Justice Project’s Rule of Law Index**, using data from *Our World in Data (OWID)*.  
Includes:
- Data preprocessing and cleaning with pandas.  
- GeoPandas / Plotly visualisation.  
- Year selector interactivity (slider).

> Demonstrates **K54**, **S50**, and **S55** through visual storytelling and data exploration.

---

### 3. [Data Pipeline CI](./DAT5501_lab/DataPipelineCI/README.md)
A demonstration of a **Continuous Integration (CI)** setup for a data-analysis workflow.  
Includes:
- Unit testing a line-fitting model.  
- Integration with CircleCI or GitHub Actions.  
- Synthetic data generation and validation.

> Demonstrates **S53** and **K57** through automated testing and reproducible pipelines.

---

## ⚙️ Setup Instructions

1. Clone this repository:
   ```bash
   git clone https://github.com/<your-username>/DAT5501_lab.git
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
