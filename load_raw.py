import polars as pl
import sqlite3
import os

# Paths
data_dir = "C:/Users/eden_/OneDrive/Desktop/ks5dash/data"
db_path = "C:/Users/eden_/OneDrive/Desktop/ks5dash/schools.db"

# Connect to SQLite
conn = sqlite3.connect(db_path)

# Years to load
years = [2022, 2023, 2024]

for year in years:
    xlsx_path = os.path.join(data_dir, f"ks5_{year - 2000}.xlsx")  # e.g., ks5_19.xlsx
    if not os.path.exists(xlsx_path):
        print(f"Skipping {year} - file not found")
        continue
    
    # Read XLSX with Polars
    df = pl.read_excel(xlsx_path, engine="openpyxl")  # Requires 'openpyxl' package
    # Add year column
    df = df.with_columns(pl.lit(year).alias("year"))
    
    # Rename columns to match schema (adjust these based on your XLSX headers)
    df = df.rename({
        "URN": "urn",
        "SUBJECT": "subject_code",
        "ENTRIES": "entries",
        "%_A*": "grade_a_star",
        "%_A": "grade_a",
        "%_B": "grade_b",
        "%_C": "grade_c",
        "%_D": "grade_d",
        "%_E": "grade_e"
    }).select([
        "urn", "year", "subject_code", "entries",
        "grade_a_star", "grade_a", "grade_b", "grade_c", "grade_d", "grade_e"
    ])
    
    # Write to SQLite
    df.write_database("ks5_raw", conn, if_exists="append")
    print(f"Loaded {year} - {len(df)} rows")

conn.close()
print("Data load complete!")