# 🗳️ US Primary Election Vote Analysis (2016)

## 📘 Overview
This project analyses the 2016 US Primary Election dataset to explore **state-level voting patterns** and **candidate comparisons**.  
It showcases professional data analysis practices using **Python, Pandas, and Matplotlib**, including unit testing and modular code design.

The workflow automatically identifies the **top two candidates by total votes** and compares their vote fractions across states.  
All major functions are unit-tested to verify accuracy and reliability, aligning with professional data analytics standards and the DAT5501 module’s learning outcomes.

---

## 🧩 Learning Objectives
- Load and clean **semicolon-separated CSV** data.
- Perform **grouped and weighted aggregations** using Pandas.
- Visualise data with **histograms** and **scatter plots**.
- Implement **unit tests** to validate key data-processing functions.
- Apply **structured repository management** and documentation practices.
- Use code design patterns that enable **reusability and testing**.

---

## 🧠 Knowledge, Skills, and Behaviours (KSBs) Evidenced

| Category | Code | Description | Evidence |
|-----------|------|-------------|-----------|
| **Knowledge** | K54 | Critically analyse and interpret data from diverse datasets | Weighted state-level vote analysis |
| | K57 | Apply data-driven approaches to processing and decision-making | Aggregation and fraction computation logic |
| | K59 | Apply data analytics to solve business or social problems | Comparing performance of political candidates |
| | K60 | Recognise and mitigate data bias and compliance issues | Accurate treatment of vote fractions |
| **Skills** | S49 | Apply data analysis techniques appropriately | Exploratory and confirmatory data aggregation |
| | S50 | Communicate and visualise results effectively | Clear, labelled Matplotlib charts |
| | S53 | Validate and test analysis results | PyTest unit tests verifying logic |
| | S55 | Use standard industry tools to analyse large datasets | Pandas and Matplotlib implementation |
| **Behaviours** | B1 | Maintain clarity and professionalism in technical work | Structured repository, documentation, and code comments |

---

## 🧰 Technologies Used
- **Python 3.13**
- **Pandas** – Data cleaning, grouping, and analysis  
- **Matplotlib** – Data visualisation  
- **PyTest** – Unit testing framework  
- **Pathlib / OS** – Path management and reproducibility  

---

## 📂 File Structure
```
DAT5501_lab/
│
├── USelection/
│   ├── us_election.py          # Main analysis script
│   ├── test_us_election.py     # Unit tests for core functions
│   ├── US-2016-primary (1).csv # Dataset (semicolon-separated)
│   ├── README.md               # Project documentation (this file)
│   └── figures/                # Optional folder for saved charts
│
└── venv/                       # Python virtual environment (excluded from Git)
```

---

## 🧮 Code Design and Testing

### Core Functions
| Function | Purpose |
|-----------|----------|
| `load_election_csv()` | Safely loads semicolon-delimited CSVs |
| `top_two_candidates()` | Identifies top-2 candidates by total votes |
| `compute_state_fraction()` | Calculates weighted vote fraction per state |
| `compare_two_candidates()` | Produces side-by-side state-level comparison |

### Unit Tests
| Test Name | Description |
|------------|--------------|
| `test_load_election_csv_semicolon()` | Confirms correct parsing of `;`-delimited data |
| `test_top_two_candidates_order()` | Ensures correct ranking by total votes |
| `test_compute_state_fraction_weighted()` | Verifies weighted average accuracy |
| `test_compare_two_candidates_alignment()` | Checks alignment and validity of comparison table |

### Run Tests
```bash
# Activate virtual environment
source ../../venv/bin/activate

# From USelection directory
pytest -q