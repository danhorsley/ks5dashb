import polars as pl
import sqlite3
import os

# Paths
data_dir = "C:/Users/eden_/OneDrive/Desktop/ks5dashb/data"
db_path = "C:/Users/eden_/OneDrive/Desktop/ks5dashb/schools.db"

# Connect to SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS schools")

# Create schools table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS schools (
        urn TEXT PRIMARY KEY,
        school_name TEXT,
        postcode TEXT,
        age_low INTEGER,
        age_high INTEGER,
        gender TEXT,
        sch_status TEXT,
        local_authority TEXT,
        rel_char TEXT,
        school_type TEXT,
        minor_group TEXT,
        region TEXT  -- Use LANAME as region initially
    )
""")

# Load .xlsx
xlsx_path = os.path.join(data_dir, "england_school_information.xlsx")
if os.path.exists(xlsx_path):
    df = pl.read_excel(xlsx_path, engine="openpyxl")
    
    # Rename columns to match schema
    df = df.rename({
        "URN": "urn",
        "SCHNAME": "school_name",
        "POSTCODE": "postcode",
        "AGELOW": "age_low",
        "AGEHIGH": "age_high",
        "GENDER": "gender",
        "SCHSTATUS": "sch_status",
        "LANAME": "local_authority",
        "RELCHAR": "rel_char",
        "SCHOOLTYPE": "school_type",
        "MINORGROUP": "minor_group"
    }).select([
        "urn", "school_name", "postcode", "age_low", "age_high", "gender",
        "sch_status", "local_authority", "rel_char", "school_type", "minor_group"
    ])
    
    # Map school_type (simple rule, adjust if needed)
    # df = df.with_columns(
    #     pl.when(pl.col("school_type").str.contains("Independent"))
    #     .then(pl.lit("Independent"))
    #     .otherwise(pl.lit("State")).alias("school_type")
    # )
    
    # Set region as local_authority for now
    df = df.with_columns(pl.col("local_authority").alias("region"))
    
    # Filter for post-16 schools (KS5-relevant)
    df = df.filter(pl.col("age_high") >= 16)
    
    # Write to SQLite
    df.to_pandas().to_sql("schools", conn, if_exists="replace", index=False)
    print(f"Loaded schools - {len(df)} rows")

conn.commit()
conn.close()
print("Schools load complete!")