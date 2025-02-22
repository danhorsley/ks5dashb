import pandas as pd
import sqlite3
import os

# Paths
data_dir = "C:/Users/eden_/OneDrive/Desktop/ks5dashb/data"
db_path = "C:/Users/eden_/OneDrive/Desktop/ks5dashb/schools.db"

# Connect to SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create gias_schools table (without open_date)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS gias_schools (
        urn TEXT PRIMARY KEY,
        school_name TEXT,
        school_capacity INTEGER,
        number_students INTEGER,
        num_girls INTEGER,
        num_boys INTEGER,
        gender TEXT,
        is_selective INTEGER,
        website TEXT,
        head TEXT,
        establishment_type TEXT,
        phase_of_education TEXT,
        statutory_low_age INTEGER,
        statutory_high_age INTEGER,
        religious_character TEXT,
        local_authority TEXT,
        postcode TEXT
    )
""")

# Load .xlsx (e.g., gias_2025.xlsx) with pandas (default engine)
xlsx_path = os.path.join(data_dir, "gias_2025.xlsx")  # Adjust filename
if os.path.exists(xlsx_path):
    # Read with pandas, no strict type inference
    df = pd.read_excel(xlsx_path)
    
    # Rename columns to match schema (adjust based on headers)
    df = df.rename(columns={
        "URN": "urn",
        "EstablishmentName": "school_name",
        "SchoolCapacity": "school_capacity",
        "NumberOfPupils": "number_students",
        "NumberOfBoys": "num_boys",
        "NumberOfGirls": "num_girls",
        "Gender (name)": "gender",
        "AdmissionsPolicy (name)": "admissions_policy",  # Temporary for is_selective derivation
        "SchoolWebsite": "website",
        "HeadTitle (name)": "head_title",
        "HeadFirstName": "head_first_name",
        "HeadLastName": "head_last_name",
        "TypeOfEstablishment (name)": "establishment_type",
        "PhaseOfEducation (name)": "phase_of_education",
        "StatutoryLowAge": "statutory_low_age",
        "StatutoryHighAge": "statutory_high_age",
        "ReligiousCharacter (name)": "religious_character",
        "LA (name)": "local_authority",
        "Postcode": "postcode"
    })
    
    # Select required columns (without open_date)
    df = df[[
        "urn", "school_name", "school_capacity", "number_students", "num_boys", "num_girls", "gender",
        "admissions_policy", "website", "head_title", "head_first_name", "head_last_name", "establishment_type",
        "phase_of_education", "statutory_low_age", "statutory_high_age", "religious_character", "local_authority", "postcode"
    ]]
    
    # Derive is_selective (1 if "Selective", 0 if "Non-selective", "Not applicable", or NaN)
    df['is_selective'] = df['admissions_policy'].apply(
        lambda x: 1 if pd.notna(x) and isinstance(x, str) and "Selective" in x else 0
    )
    
    # Combine headteacher name, handling NaN/blank values
    df['head'] = df[['head_title', 'head_first_name', 'head_last_name']].agg(
        lambda x: ' '.join(filter(None, [str(v).strip() if pd.notna(v) else '' for v in x])), axis=1
    )
    df = df.drop(columns=['head_title', 'head_first_name', 'head_last_name'])
    
    # Filter for KS5-relevant schools (post-16)
    df = df[df['statutory_high_age'] >= 16]
    
    # Write to SQLite directly from Pandas, handling nulls as None
    df.to_sql("gias_schools", conn, if_exists="replace", index=False)
    print(f"Loaded GIAS schools - {len(df)} rows")

conn.commit()
conn.close()
print("GIAS schools load complete!")