"""
Utility functions for data processing
Updated to show BEFORE and AFTER states clearly
"""

import os
import pandas as pd
import numpy as np
import json


def ensure_directory(path):
    """Create directory if it doesn't exist"""
    os.makedirs(path, exist_ok=True)


def load_csv(file_path):
    """Load CSV file with error handling"""
    try:
        df = pd.read_csv(file_path)
        print(f"✓ Loaded: {file_path} ({len(df)} rows, {len(df.columns)} columns)")
        return df
    except Exception as e:
        print(f"✗ Error loading {file_path}: {e}")
        return pd.DataFrame()


def save_csv(df, file_path):
    """Save DataFrame to CSV"""
    try:
        df.to_csv(file_path, index=False)
    except Exception as e:
        print(f"✗ Error saving CSV {file_path}: {e}")


def save_json(df, file_path):
    """Save DataFrame to JSON"""
    try:
        df.to_json(file_path, orient='records', indent=2, date_format='iso')
    except Exception as e:
        print(f"✗ Error saving JSON {file_path}: {e}")


def report_quality_before(df, label="Dataset"):
    """
    Report initial data quality BEFORE any transformations
    Focus on missing values and duplicates as required by assignment
    """
    print(f"\n{'─'*70}")
    print(f"DATA QUALITY BEFORE TRANSFORMATION: {label}")
    print(f"{'─'*70}\n")
    
    print(f"📊 Dataset Shape: {len(df)} rows × {len(df.columns)} columns\n")
    
    # ===== MISSING VALUES (DETAILED) =====
    print(f"🔍 MISSING VALUES:")
    print(f"{'─'*70}")
    
    total_missing = 0
    missing_details = {}
    
    for col in df.columns:
        # Count different types of missing
        null_count = df[col].isnull().sum()
        empty_count = 0
        na_variant_count = 0
        
        if df[col].dtype == 'object':
            # Count empty strings (before normalization)
            empty_count = (df[col].astype(str).str.strip() == '').sum()
            
            # Count NA variants
            na_variant_count = df[col].isin(['NA', 'N/A', 'null', 'None', 'nan']).sum()
        
        col_total = null_count + empty_count + na_variant_count
        total_missing += col_total
        
        if col_total > 0:
            percent = (col_total / len(df)) * 100
            print(f"   • {col}: {col_total} ({percent:.2f}%)")
            
            if empty_count > 0:
                print(f"      └─ includes {empty_count} empty strings")
            if na_variant_count > 0:
                print(f"      └─ includes {na_variant_count} NA variants")
            
            missing_details[col] = {
                'total': col_total,
                'null': null_count,
                'empty': empty_count,
                'na_variants': na_variant_count
            }
    
    if total_missing == 0:
        print("   ✓ No missing values detected")
    else:
        print(f"\n   📈 TOTAL MISSING VALUES: {total_missing}")
    
    # ===== DUPLICATE RECORDS =====
    print(f"\n🔍 DUPLICATE RECORDS:")
    print(f"{'─'*70}")
    
    duplicates = df.duplicated().sum()
    dup_percent = (duplicates / len(df)) * 100 if len(df) > 0 else 0
    
    print(f"   • Exact duplicate rows: {duplicates} ({dup_percent:.2f}%)")
    print(f"   ⚠️  Note: More may be found after normalizing missing values\n")
    
    return total_missing, duplicates


def report_quality_after(df, label, initial_rows, final_rows, duplicates_removed):
    """
    Report data quality AFTER transformations
    Show clear before → after summary
    """
    print(f"\n{'─'*70}")
    print(f"TRANSFORMATION SUMMARY: {label}")
    print(f"{'─'*70}\n")
    
    final_missing = df.isnull().sum().sum()
    final_duplicates = df.duplicated().sum()
    
    print(f"📊 CHANGES:")
    print(f"   • Rows: {initial_rows} → {final_rows} (removed {initial_rows - final_rows})")
    print(f"   • Duplicate rows removed: {duplicates_removed}")
    print(f"   • Missing values remaining: {final_missing}")
    print(f"   • Duplicate rows remaining: {final_duplicates}")
    
    if final_missing == 0:
        print(f"\n   ✅ All missing values handled!")
    
    if final_duplicates == 0:
        print(f"   ✅ All duplicates removed!")
    
    print()


def report_quality(df, label="Dataset"):
    """
    Generic quality report (for compatibility with old code)
    Shows basic stats only
    """
    print(f"\n{'─'*60}")
    print(f"Quality Report: {label}")
    print(f"{'─'*60}")
    
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    
    missing_total = df.isnull().sum().sum()
    print(f"Missing Values: {missing_total}")
    
    duplicates = df.duplicated().sum()
    print(f"Duplicates: {duplicates}")
    print(f"{'─'*60}\n")