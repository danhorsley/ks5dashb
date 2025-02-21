import polars as pl
import sqlite3
import os
import re

# Paths
data_dir = "C:/Users/eden_/OneDrive/Desktop/ks5dashb/data"
db_path = "C:/Users/eden_/OneDrive/Desktop/ks5dashb/schools.db"

# Connect to SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create enrollment_outcomes table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS enrollment_outcomes (
        urn TEXT,
        year INTEGER,
        total_cohort INTEGER,
        l3_cohort INTEGER,
        total_he INTEGER,
        total_fe INTEGER,
        total_employment INTEGER,
        PRIMARY KEY (urn, year)
    )
""")

# Years to load (adjust based on available files)
years = [2022, 2023, 2024]
for year in years:
    xlsx_path = os.path.join(data_dir, f"england_ks5-students_{year}.xlsx")
    if os.path.exists(xlsx_path):
        df = pl.read_excel(xlsx_path, engine="openpyxl")
        
        # Rename columns to match schema (adjust based on headers)
        df = df.rename({
            "URN": "urn",
            "TOT_COHORT": "total_cohort",
            "L3_COHORT": "l3_cohort",
            "TOT_HE": "total_he",
            "TOT_FE": "total_fe",
            "TOT_EMPLOYMENT": "total_employment"
        }).select([
            "urn", "total_cohort", "l3_cohort", "total_he", "total_fe", "total_employment"
        ])
        
        # Add year (derived from filename)
        df = df.with_columns(pl.lit(year).alias("year"))
        
        # Write to SQLite
        df.to_pandas().to_sql("enrollment_outcomes", conn, if_exists="append", index=False)
        print(f"Loaded enrollment outcomes for {year} - {len(df)} rows")

conn.commit()
conn.close()
print("Enrollment outcomes load complete!")