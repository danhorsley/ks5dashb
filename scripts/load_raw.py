import polars as pl
import sqlite3
import os

# Paths
data_dir = "C:/Users/eden_/OneDrive/Desktop/ks5dashb/data"
db_path = "C:/Users/eden_/OneDrive/Desktop/ks5dashb/schools.db"

# Connect to SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create ks5_raw table if it doesn’t exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS ks5_raw (
        urn TEXT,
        year INTEGER,
        subject TEXT,
        grade TEXT,
        number_exams TEXT
    )
""")
conn.commit()

# Years to load
#years = [2022, 2023, 2024]
years = [2024]
for year in years:
    xlsx_path = os.path.join(data_dir, f"ks5_{year}.xlsx")
    if not os.path.exists(xlsx_path):
        print(f"Skipping {year} - file not found")
        continue
    # Read XLSX
    df = pl.read_excel(xlsx_path, engine="openpyxl")
    df = df.with_columns(pl.lit(year).alias("year"))

    # Rename columns (adjust to your exact headers)
    df = df.rename({
        "URN": "urn",
        "Subject": "subject",
        "Grade/Total entries": "grade",
        "Number of exams": "number_exams"  # Update these based on your file
    }).select([
        "urn", "year", "subject", "grade", "number_exams"
    ])

    # Convert number_exams to integer
    #df = df.with_columns(pl.col("number_exams").cast(pl.Int64))

    # Write to SQLite
    df.to_pandas().to_sql("ks5_raw", conn, if_exists="append", index=False)
    print(f"Loaded {year} - {len(df)} rows")

conn.close()
print("Data load complete!")