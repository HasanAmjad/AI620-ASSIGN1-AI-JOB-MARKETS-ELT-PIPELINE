
# AI Labor Markets – Modern ELT Pipeline
AI 620 – Data Engineering for AI Systems
Assignment 1

---

## Project Overview

This project implements a modular ELT (Extract, Load, Transform) pipeline focused on the AI Labor Markets domain.

The pipeline integrates multiple real-world data sources to analyze:

- AI job demand trends
- Salary distribution patterns
- Skill requirements
- Geographic structure
- Relationship between hiring activity and search interest

Note: The analysis of this project assignment is done in the notebooks folder, which answers major questions.

---


## Data Sources

1. Adzuna Jobs API (API Source)
   - Real-time AI job listings
   - Salary ranges
   - Location and contract type
   - Posting timestamps
   - Semi-structured JSON format

2. Kaggle AI Jobs Dataset (Public Dataset)
   - Structured CSV dataset
   - Job titles
   - Salary information
   - Identified skills
   - Employment type

3. Google Trends (Time-Series Data)
   - Keywords: AI jobs, machine learning jobs, data scientist salary
   - Timeframe: today 5-y (last 5 years)
   - Provides indexed search interest over time

---

## Pipeline Architecture

Extract → Load → Transform → Analyze → Visualize

Data Flow:

[Adzuna API] [Kaggle Dataset] ---> ELT Pipeline ---> Cleaned Data ---> Analysis
[Google Trends] /

---

## Project Structure
project/
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── cleaned/
│
├── src/
│   ├── extract_api.py
│   ├── extract_kaggle.py
│   ├── extract_trends.py
│   ├── transform.py
│
├── notebooks/
│   └── analysis.ipynb
│
├── run_pipeline.py
├── requirements.txt
├── .env
└── README.md
---

## Setup Instructions

1. Clone the Repository

git clone <repository_url>
cd project

2. Create Virtual Environment

Windows:
python -m venv venv
venv\Scripts\activate

Mac/Linux:
python3 -m venv venv
source venv/bin/activate

3. Install Dependencies

pip install -r requirements.txt

Required Libraries:
- pandas
- matplotlib
- seaborn
- requests
- pytrends
- python-dotenv

4. Configure Environment Variables

Create a .env file in the root directory:

ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_app_key

API credentials are loaded securely using environment variables and are not hard-coded.

5. Run the Pipeline

python run_pipeline.py

This performs:
- Extraction from Adzuna API
- Loading Kaggle dataset
- Extraction from Google Trends
- Storage of raw files in data/raw/
- Processing and structuring into data/processed/
- Cleaning and feature engineering into data/cleaned/

---

## Data Engineering Decisions

Data Heterogeneity:
- Adzuna provides semi-structured JSON
- Kaggle provides structured CSV
- Google Trends provides indexed time-series data

Schema Harmonization:
All date fields were standardized into a unified 'date' column for temporal consistency.

Cleaning and Transformation:
- Salary converted to numeric format
- Duplicate records removed
- Skill count feature engineered
- Binary indicators created (remote, full-time)
- Monthly and weekly time aggregations applied
- Outliers filtered for improved visualization clarity

Storage Strategy:
- JSON preserves nested API structure
- CSV supports readability and analysis
- Cleaned datasets enable reproducibility

---

## Key Analysis Performed

- Monthly AI job posting trends
- Salary distribution comparison (Kaggle vs Adzuna)
- Top 15 highest-paying AI job titles
- Skill count vs salary relationship (correlation ≈ 0.28)
- Multi-feature correlation matrix
- Correlation between job postings and Google Trends search interest

---

## Core Insights

- Skill count shows a weak positive correlation with salary.
- Multi-skilled AI roles tend to command higher compensation.
- Hiring activity exhibits temporal variation.
- Search interest demonstrates measurable association with job demand.
- Geographic structure influences salary patterns.

---

## Limitations

- Limited API pagination restricts dataset size.
- Google Trends provides relative rather than absolute demand.
- Kaggle dataset lacks seniority-level information.
- API results may be regionally biased.

---
