"""Utility helpers for loading and saving text, CSV, and JSON data.

Summary:
    This module provides convenience functions for reading plain text and CSV
    files into strings, loading CSV data with pandas, and writing text or JSON
    outputs to disk. It is designed for lightweight data ingestion and export
    in inspection/finding triage workflows.

Author: Mulugeta W.A.
Date: 2026-08-24
"""

import os
import json
import csv
from pathlib import Path
import pandas as pd
import numpy as np
from tqdm import tqdm
from datetime import datetime
from typing import List, Optional

def dict2str_serialize(row_data: dict):
    return ' '.join(f"{k}: {v}" for k, v in row_data.items())

def load_textfile(filepath: str | Path):
    """read the markdown and text file"""
    
    print(f"loading {filepath}...")
    try:
        if str(filepath).endswith(".csv"):
            with open(filepath, mode='r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file) # create DictReader
                data_content = []  # List to store dictionaries
                for row in csv_reader:
                    data_content.append(dict2str_serialize(row)) # convert into header: value pair and merge in a single string
                data_content = ' \n'.join([r for r in data_content]) # combine rows into single string with \n breakline
        else:
            with open(filepath, "r", encoding="utf-8") as file:
                data_content = file.read()
        
        return data_content
    except Exception as ex:
        print(f"ERROR: load_textfile: {ex}")
    return ''

def save_textfile(data: str, filepath: str | Path):
    print(f"saving {filepath}...")
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(data)
    except Exception as ex:
        print(f"ERROR: save_textfile: {ex}")

def load_csv(filepath: str | Path, index_col:int = None):
    print(f"loading {filepath}...")
    try:
        return pd.read_csv(filepath, index_col=index_col).apply(lambda col: pd.to_datetime(col, errors="ignore") if col.dtypes == "object" else col)  # Automatically find and convert all date-like string columns
    except Exception as ex:
        print(f"ERROR: load_csv: {ex}")
        
def save_json(data: dict, filepath: str | Path):
    print(f"saving {filepath}...")
    try:
        with open(filepath, 'w') as file:
            file.write(json.dumps(data, indent=4, sort_keys=False))
            file.close()
    except Exception as ex:
            print(f"ERROR: save_json: {ex}")
            