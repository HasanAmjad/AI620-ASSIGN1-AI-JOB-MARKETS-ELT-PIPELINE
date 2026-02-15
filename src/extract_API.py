import os
import json

import pandas as pd
import requests

from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

RAW_PATH = "data/raw"
PROCESSED_PATH = "data/processed"


def extract_API_data():

    print("Extracting Adzuna API data...")

    os.makedirs(RAW_PATH, exist_ok=True)
    os.makedirs(PROCESSED_PATH, exist_ok=True)

    app_id = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")
    

    if not app_id or not app_key:
        raise ValueError("Adzuna API credentials not found in environment variables.")

    keyword = "machine learning engineer"
    country = "us"
    pages = 10
    results_per_page = 150

    all_results = []

    for page in range(1, pages + 1):

        url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/{page}"

        params = {
            "app_id": app_id,
            "app_key": app_key,
            "what": keyword,
            "results_per_page": results_per_page,
            "content-type": "application/json"
        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            raise Exception(
                f"API request failed: {response.status_code}, {response.text}"
            )

        data = response.json()
        all_results.extend(data.get("results", []))

    # -------- Save RAW JSON --------
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_file = os.path.join(RAW_PATH, f"adzuna_raw_{timestamp}.json")

    with open(raw_file, "w") as f:
        json.dump(all_results, f, indent=4)

    print("Raw API data saved.")

    # -------- Minimal Structuring (NOT cleaning) --------
    records = []

    for job in all_results:
        records.append({
            "id": job.get("id"),
            "title": job.get("title"),
            "company": job.get("company", {}).get("display_name"),
            "location": job.get("location", {}).get("display_name"),
            "salary_min": job.get("salary_min"),
            "salary_max": job.get("salary_max"),
            "created": job.get("created"),
            "category": job.get("category", {}).get("label")
        })

    df = pd.DataFrame(records)

    # -------- Save PROCESSED --------
    df.to_csv(os.path.join(PROCESSED_PATH, "adzuna_jobs.csv"), index=False)
    df.to_json(
        os.path.join(PROCESSED_PATH, "adzuna_jobs.json"),
        orient="records"
    )

    print("Processed API files saved.")

    return df