import os
import pandas as pd
import ast
from src.utils import ensure_directory, load_csv, save_csv, save_json, report_quality

PROCESSED_PATH = "data/processed"
CLEANED_PATH = "data/cleaned"


def transform_all():

    ensure_directory(CLEANED_PATH)

    processed_files = [
        f for f in os.listdir(PROCESSED_PATH)
        if f.endswith(".csv")
    ]

    for file in processed_files:

        print("\n====================================")
        print(f"Transforming: {file}")
        print("====================================")

        df = load_csv(os.path.join(PROCESSED_PATH, file))

        # -----------------------------------
        # Normalize whitespace + placeholders
        # -----------------------------------
        df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)
        df = df.replace(r"^\s*$", pd.NA, regex=True)
        df = df.replace(["NA", "N/A", "null", "None"], pd.NA)

        report_quality(df, f"{file} BEFORE")

        # -----------------------------------
        # Remove exact duplicates
        # -----------------------------------
        df = df.drop_duplicates()

        # -----------------------------------
        # Detect & convert date columns
        # -----------------------------------
        for col in df.columns:
            if any(k in col.lower() for k in ["date", "created", "time"]):
                df[col] = pd.to_datetime(df[col], errors="coerce")

        # -----------------------------------
        # Detect & convert numeric-like columns
        # -----------------------------------
        for col in df.columns:
            if any(k in col.lower() for k in ["salary", "min", "max", "amount", "value"]):
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # -----------------------------------
        # Detect list-like string columns
        # -----------------------------------
        for col in df.columns:
            if df[col].dtype == object:
                sample = df[col].dropna().astype(str).head(5)
                if any(s.startswith("[") and s.endswith("]") for s in sample):

                    def parse_list(x):
                        try:
                            return ast.literal_eval(x)
                        except:
                            return []

                    df[col] = df[col].apply(parse_list)

        # -----------------------------------
        # Treat empty lists as missing
        # -----------------------------------
        for col in df.columns:
            if df[col].apply(lambda x: isinstance(x, list)).any():
                empty_lists = df[col].apply(
                    lambda x: isinstance(x, list) and len(x) == 0
                )
                if empty_lists.sum() > 0:
                    print(f"{col} empty lists treated as missing:", empty_lists.sum())
                    df.loc[empty_lists, col] = pd.NA

        # -----------------------------------
        # Drop rows with >= 2 missing values
        # -----------------------------------
        missing_per_row = df.isna().sum(axis=1)
        rows_before = len(df)
        df = df[missing_per_row < 2]
        rows_after = len(df)

        print("Rows dropped (2+ missing fields):", rows_before - rows_after)

        # -----------------------------------
        # Impute remaining numeric columns (median)
        # -----------------------------------
        numeric_cols = df.select_dtypes(include=["number"]).columns
        for col in numeric_cols:
            df[col] = df[col].fillna(df[col].median())

        # -----------------------------------
        # Fill remaining text columns with 'Unknown'
        # -----------------------------------
        text_cols = df.select_dtypes(include=["object"]).columns
        for col in text_cols:
            df[col] = df[col].fillna("Unknown")

        report_quality(df, f"{file} AFTER")

        # -----------------------------------
        # Save cleaned dataset
        # -----------------------------------
        output_name = file.replace(".csv", "_cleaned.csv")

        save_csv(df, os.path.join(CLEANED_PATH, output_name))
        save_json(df, os.path.join(CLEANED_PATH, output_name.replace(".csv", ".json")))

        print(f"{file} cleaned and saved successfully.")