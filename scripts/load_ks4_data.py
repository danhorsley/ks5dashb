import pandas as pd

def split_double_grade(row):
    """Split Double Award grades (e.g., '8-7' or '87') into two lines."""
    grade = row["grade_desc"]
    entries = row["entries"]
    dc = row["discount_code"]
    if "-" in grade:  # Handle "8-7" format
        g1, g2 = map(int, grade.split("-"))
    else:  # Handle shorthand like "87"
        if len(grade) == 2 and grade.isdigit():  # Assume "87" means "8-7"
            g1, g2 = int(grade[0]), int(grade[1])
        elif grade == 'U' and dc == 'RA1E':
            g1, g2 = 0, 0
        elif grade == 'No Result':
            g1, g2 = 0 , 0
        elif grade == 'Covid impacted':
            g1, g2 = 0 , 0
        else:
            g1, g2 = int(grade), int(grade)  # Fallback for single digits or errors
    return [
        {**row, "grade": g1, "entries": entries},
        {**row, "grade": g2, "entries": entries}
    ]

def load_ks4_data(file_path):
    """
    Load, clean, and preprocess KS4 data from a CSV file.
    
    Returns a pandas DataFrame with standardized columns and processed grades.
    """
    # Load the CSV
    df = pd.read_csv(file_path, encoding='latin1')  # or encoding='cp1252'
    
    # Rename columns for consistency
    df.columns = ["urn", "school_name", "inst_type", "cohort_size", "qual", "qual_desc", 
                  "grade_struct", "discount_code", "subject_group", "subject", "grade", 
                  "grade_desc", "entries"]
    
    # Filter out total rows and keep only grade-specific data
    df_grades = df[df["grade"] != "Total number entered"]
    
    # Handle Double Science (split into two lines)
    df_double = df_grades[df_grades["subject"] == "Science: Double Award"]
    if not df_double.empty:
        split_rows = df_double.apply(split_double_grade, axis=1).explode().tolist()
        df_split = pd.DataFrame(split_rows)
    else:
        df_split = pd.DataFrame()
    
    # Handle other qualifications (non-Double Science)
    df_other = df_grades[df_grades["subject"] != "Science: Double Award"]
    
    # Combine processed Double Science with other data
    df_clean = pd.concat([df_other, df_split], ignore_index=True)
    
    # Rough mapping for BTEC grades (optional, for averaging)
    btec_mapping = {
        "*2": 8.5, "D2": 7.5, "M2": 5.5, "P2": 4.5,
        "D1": 3.5, "M1": 2.5, "P1": 1.5, "U": 0
    }
    df_clean.loc[df_clean["qual"].str.contains("BTEC"), "mapped_grade"] = \
        df_clean[df_clean["qual"].str.contains("BTEC")]["grade"].map(btec_mapping)
    
    # Categorize subjects into STEM, Arts, Humanities
    subject_categories = {
        "Science: Double Award": "STEM", "Health Studies": "STEM",
        "Art & Design (Fine Art)": "Arts", "Speech & Drama": "Arts",
        "English Language": "Humanities", "Arabic": "Humanities"
    }
    df_clean["category"] = df_clean["subject"].map(subject_categories).fillna("Other")
    
    # Add key_stage marker
    df_clean["key_stage"] = "KS4"
    
    # Ensure numeric columns are correct
    df_clean["entries"] = pd.to_numeric(df_clean["entries"], errors="coerce")
    df_clean["grade"] = pd.to_numeric(df_clean["grade"], errors="coerce")
    
    # Drop rows with NaN entries if any (optional cleanup)
    df_clean = df_clean.dropna(subset=["entries"])
    
    return df_clean

if __name__ == "__main__":
    # Example usage
    file_path = "C:/Users/eden_/OneDrive/Desktop/ks5dashb/data/ks4_data.csv"  # Replace with your actual file path
    ks4_data = load_ks4_data(file_path)
    print("KS4 data loaded and processed successfully!")
    print(ks4_data.head())  # Preview the first few rows
    # Optionally save to a new CSV for later use
    ks4_data.to_csv("processed_ks4_data.csv", index=False)