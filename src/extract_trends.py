import os
import pandas as pd
from pytrends.request import TrendReq

RAW_PATH = "data/raw"
PROCESSED_PATH = "data/processed"

def extract_trends_data():

    print("Extracting Google Trends data...")

    pytrends = TrendReq(hl='en-US', tz=360)

    keywords = ["AI jobs", "machine learning jobs", "data scientist salary"]

    pytrends.build_payload(keywords, timeframe='today 5-y')

    trends_data = pytrends.interest_over_time()

    if trends_data.empty:
        print("No data retrieved.")
        return

    os.makedirs(RAW_PATH, exist_ok=True)
    os.makedirs(PROCESSED_PATH, exist_ok=True)

    trends_data.to_csv(os.path.join(RAW_PATH, "google_trends_raw.csv"))

    trends_data.reset_index(inplace=True)
    trends_data.to_csv(os.path.join(PROCESSED_PATH, "google_trends_processed.csv"), index=False)
    trends_data.to_json(os.path.join(PROCESSED_PATH, "google_trends_processed.json"), orient="records")

    print("Google Trends data saved successfully.")