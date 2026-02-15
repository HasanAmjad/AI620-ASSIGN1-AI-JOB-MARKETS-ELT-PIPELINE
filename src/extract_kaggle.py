import os
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi

RAW_PATH = "data/raw"
PROCESSED_PATH = "data/processed"
DATASET = "abhaykumar2812/ai-and-ml-jobs"


def extract_kaggle_data():

    os.makedirs(RAW_PATH, exist_ok=True)
    os.makedirs(PROCESSED_PATH, exist_ok=True)

    # Check if dataset already exists
    existing_csvs = [f for f in os.listdir(RAW_PATH) if f.endswith(".csv")]

    if existing_csvs:
        print("Kaggle dataset already downloaded. Skipping download.")
    else:
        print("Downloading Kaggle dataset...")

        api = KaggleApi()
        api.authenticate()

        api.dataset_download_files(DATASET, path=RAW_PATH, unzip=True)
        print("Download complete.")

    # Load first CSV
    files = [f for f in os.listdir(RAW_PATH) if f.endswith(".csv")]

    if not files:
        raise FileNotFoundError("No CSV file found in raw directory.")

    file_path = os.path.join(RAW_PATH, files[0])
    df = pd.read_csv(file_path)

    # Save processed formats
    df.to_csv(os.path.join(PROCESSED_PATH, "kaggle_jobs.csv"), index=False)
    df.to_json(
        os.path.join(PROCESSED_PATH, "kaggle_jobs.json"),
        orient="records"
    )

    print("Processed files saved.")

    return df