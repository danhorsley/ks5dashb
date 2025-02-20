import sqlite3

conn = sqlite3.connect("C:/Users/eden_/OneDrive/Desktop/ks5dashb/schools.db")
cursor = conn.cursor()

# Create summary table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS ks5_school_summary (
        urn TEXT,
        year INTEGER,
        total_entries INTEGER,
        avg_grade REAL,
        stem_avg_grade REAL,
        arts_avg_grade REAL,
        PRIMARY KEY (urn, year)
    )
""")

# Aggregate, handling "supp"
cursor.execute("""
    INSERT OR REPLACE INTO ks5_school_summary
    SELECT 
        urn,
        year,
        SUM(CAST(CASE WHEN number_exams = 'supp' THEN 0 ELSE number_exams END AS INTEGER)) AS total_entries,
        SUM(CASE 
            WHEN number_exams != 'supp' AND grade = '*' THEN CAST(number_exams AS INTEGER) * 6
            WHEN number_exams != 'supp' AND grade = 'A' THEN CAST(number_exams AS INTEGER) * 5
            WHEN number_exams != 'supp' AND grade = 'B' THEN CAST(number_exams AS INTEGER) * 4
            WHEN number_exams != 'supp' AND grade = 'C' THEN CAST(number_exams AS INTEGER) * 3
            WHEN number_exams != 'supp' AND grade = 'D' THEN CAST(number_exams AS INTEGER) * 2
            WHEN number_exams != 'supp' AND grade = 'E' THEN CAST(number_exams AS INTEGER) * 1
            ELSE 0 END) / 
            NULLIF(SUM(CASE WHEN number_exams != 'supp' THEN CAST(number_exams AS INTEGER) ELSE 0 END), 0) AS avg_grade,
        SUM(CASE WHEN subject IN ('Mathematics', 'Physics', 'Chemistry', 'Biology', 'Design and Technology (Product Design)') AND number_exams != 'supp' THEN 
            CASE 
                WHEN grade = '*' THEN CAST(number_exams AS INTEGER) * 6
                WHEN grade = 'A' THEN CAST(number_exams AS INTEGER) * 5
                WHEN grade = 'B' THEN CAST(number_exams AS INTEGER) * 4
                WHEN grade = 'C' THEN CAST(number_exams AS INTEGER) * 3
                WHEN grade = 'D' THEN CAST(number_exams AS INTEGER) * 2
                WHEN grade = 'E' THEN CAST(number_exams AS INTEGER) * 1
                ELSE 0 END ELSE 0 END) / 
            NULLIF(SUM(CASE WHEN subject IN ('Mathematics', 'Physics', 'Chemistry', 'Biology', 'Design and Technology (Product Design)') AND number_exams != 'supp' THEN CAST(number_exams AS INTEGER) ELSE 0 END), 0) AS stem_avg_grade,
        SUM(CASE WHEN subject IN ('Art and Design (Fine Art)', 'Music', 'Drama and Theatre Studies') AND number_exams != 'supp' THEN 
            CASE 
                WHEN grade = '*' THEN CAST(number_exams AS INTEGER) * 6
                WHEN grade = 'A' THEN CAST(number_exams AS INTEGER) * 5
                WHEN grade = 'B' THEN CAST(number_exams AS INTEGER) * 4
                WHEN grade = 'C' THEN CAST(number_exams AS INTEGER) * 3
                WHEN grade = 'D' THEN CAST(number_exams AS INTEGER) * 2
                WHEN grade = 'E' THEN CAST(number_exams AS INTEGER) * 1
                ELSE 0 END ELSE 0 END) / 
            NULLIF(SUM(CASE WHEN subject IN ('Art and Design (Fine Art)', 'Music', 'Drama and Theatre Studies') AND number_exams != 'supp' THEN CAST(number_exams AS INTEGER) ELSE 0 END), 0) AS arts_avg_grade
    FROM ks5_raw
    GROUP BY urn, year
""")

conn.commit()
conn.close()
print("Aggregation complete!")