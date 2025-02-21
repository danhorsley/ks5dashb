import sqlite3

conn = sqlite3.connect("C:/Users/eden_/OneDrive/Desktop/ks5dashb/schools.db")
cursor = conn.cursor()

# Drop existing tables (optional, backup first)
cursor.execute("DROP TABLE IF EXISTS ks5_enrollment_summary")
cursor.execute("DROP TABLE IF EXISTS ks5_grade_summary")
cursor.execute("DROP TABLE IF EXISTS subjects")

# Create enrollment summary table (includes "supp" for total entries)
cursor.execute("""
    CREATE TABLE ks5_enrollment_summary (
        urn TEXT,
        year INTEGER,
        total_entries INTEGER,
        PRIMARY KEY (urn, year)
    )
""")

# Create grade summary table (excludes "supp" for grades)
cursor.execute("""
    CREATE TABLE ks5_grade_summary (
        urn TEXT,
        year INTEGER,
        avg_grade REAL,
        stem_avg_grade REAL,
        arts_avg_grade REAL,
        econ_avg_grade REAL,
        PRIMARY KEY (urn, year)
    )
""")
# Create subjects table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS subjects (
        subject_name TEXT PRIMARY KEY,
        category TEXT NOT NULL  -- e.g., 'STEM', 'Humanities', 'Skills', 'Arts', 'Business & Economics', 'Other'
    )
""")

# Insert categorized subjects
cursor.executescript("""
    INSERT OR REPLACE INTO subjects (subject_name, category) VALUES
    ('Accounting', 'Business & Economics'),
    ('Accounting / Finance', 'Business & Economics'),
    ('Additional Mathematics FSMQ', 'STEM'),
    ('Administrative Management', 'Skills'),
    ('Aerospace Engineering', 'STEM'),
    ('Agricultural Engineering', 'STEM'),
    ('Agriculture (General)', 'Skills'),
    ('Ancient History', 'Humanities'),
    ('Animal Care (Non-Agricultural)', 'Skills'),
    ('Animal Husbandry (Specific Animals)', 'Skills'),
    ('Applied Business', 'Business & Economics'),
    ('Applied Sciences', 'STEM'),
    ('Arabic', 'Humanities'),
    ('Arboriculture', 'Skills'),
    ('Art and Design', 'Arts'),
    ('Art and Design (3d Studies)', 'Arts'),
    ('Art and Design (Critical Studies)', 'Arts'),
    ('Art and Design (Fine Art)', 'Arts'),
    ('Art and Design (Graphics)', 'Arts'),
    ('Art and Design (Photography)', 'Arts'),
    ('Art and Design (Textiles)', 'Arts'),
    ('Automotive Engineering', 'STEM'),
    ('Baccalaureate', 'Other'),
    ('Baking / Confectionery', 'Skills'),
    ('Beauty Therapy', 'Skills'),
    ('Bengali', 'Humanities'),
    ('Biology', 'STEM'),
    ('Brickwork / Masonry', 'Skills'),
    ('Building / Construction Operations (General / Combined)', 'Skills'),
    ('Business Studies', 'Business & Economics'),
    ('Business Studies:Single', 'Business & Economics'),
    ('Chemistry', 'STEM'),
    ('Childcare Skills', 'Skills'),
    ('Chinese', 'Humanities'),
    ('Classical Civilisation', 'Humanities'),
    ('Classical Greek', 'Humanities'),
    ('Classics (General)', 'Humanities'),
    ('Computer Appreciation (Introduction)', 'STEM'),
    ('Computer Architecture / Systems', 'STEM'),
    ('Computer Games', 'STEM'),
    ('Computer Studies / Computing', 'STEM'),
    ('Computing and IT Advanced Technician', 'STEM'),
    ('Construction Carpentry / Shopfitting / Erection', 'Skills'),
    ('Dance', 'Arts'),
    ('Design and Technology', 'STEM'),
    ('Design and Technology (Engineering)', 'STEM'),
    ('Design and Technology (Product Design)', 'STEM'),
    ('Design and Technology (Textiles Technology)', 'Arts'),
    ('Drama and Theatre Studies', 'Arts'),
    ('Economics', 'Business & Economics'),
    ('Electrical installation (Buildings / Construction)', 'Skills'),
    ('Electronic / Electrical Engineering', 'STEM'),
    ('Electronics', 'STEM'),
    ('Engineering Studies', 'STEM'),
    ('English Language', 'Humanities'),
    ('English Language and Literature', 'Humanities'),
    ('English Literature', 'Humanities'),
    ('Environmental Management', 'STEM'),
    ('Environmental Science', 'STEM'),
    ('Film / Video / Television Production', 'Arts'),
    ('Film Studies', 'Arts'),
    ('Finance / Accounting (General)', 'Business & Economics'),
    ('Floristry', 'Skills'),
    ('Food Preparation (General)', 'Skills'),
    ('French', 'Humanities'),
    ('General Studies', 'Other'),
    ('Geography', 'Humanities'),
    ('Geology', 'STEM'),
    ('German', 'Humanities'),
    ('Government and Politics', 'Humanities'),
    ('Gujarati', 'Humanities'),
    ('Hairdressing Services', 'Skills'),
    ('Health Studies', 'Skills'),
    ('History', 'Humanities'),
    ('History of Art', 'Humanities'),
    ('Holistic Therapies', 'Skills'),
    ('Horses / Ponies Keeping', 'Skills'),
    ('Horticulture (General)', 'Skills'),
    ('Information and Communications Technology', 'STEM'),
    ('Italian', 'Humanities'),
    ('Japanese', 'Humanities'),
    ('Latin', 'Humanities'),
    ('Law', 'Humanities'),
    ('Law / Legal Studies', 'Humanities'),
    ('Learning Skills', 'Other'),
    ('Logic / Philosophy', 'Humanities'),
    ('Makeup', 'Skills'),
    ('Management Studies / Science', 'Business & Economics'),
    ('Manicure', 'Skills'),
    ('Manufacturing Engineering', 'STEM'),
    ('Massage Techniques (Personal Health)', 'Skills'),
    ('Mathematical Studies', 'STEM'),
    ('Mathematics', 'STEM'),
    ('Mathematics (Further)', 'STEM'),
    ('Mathematics (Numeracy)', 'STEM'),
    ('Mathematics (Statistics)', 'STEM'),
    ('Mechanical Engineering (General)', 'STEM'),
    ('Media/Film/Tv Studies', 'Arts'),
    ('Medical Science', 'STEM'),
    ('Men''s Hairdressing', 'Skills'),
    ('Modern Greek', 'Humanities'),
    ('Modern Hebrew', 'Humanities'),
    ('Motorcycle Maintenance / Repair', 'Skills'),
    ('Multimedia', 'STEM'),
    ('Music', 'Arts'),
    ('Music performance (Group)', 'Arts'),
    ('Music Technology', 'Arts'),
    ('Music Technology (Electronic)', 'Arts'),
    ('Nutrition / Diet', 'Skills'),
    ('Other Classical Languages', 'Humanities'),
    ('Other Languages', 'Humanities'),
    ('Painting and Decorating', 'Skills'),
    ('Persian', 'Humanities'),
    ('Physical Education / Sports Studies', 'Skills'),
    ('Physics', 'STEM'),
    ('Plastering', 'Skills'),
    ('Plumbing (Building Work)', 'Skills'),
    ('Polish', 'Humanities'),
    ('Portuguese', 'Humanities'),
    ('Psychology', 'Humanities'),
    ('Punjabi', 'Humanities'),
    ('Religious Education', 'Humanities'),
    ('Religious Studies', 'Humanities'),
    ('Russian', 'Humanities'),
    ('Self Development', 'Other'),
    ('Small Business Management', 'Business & Economics'),
    ('Social Science', 'Humanities'),
    ('Sociology', 'Humanities'),
    ('Sound Recording', 'Arts'),
    ('Spanish', 'Humanities'),
    ('Special Effects Makeup', 'Skills'),
    ('Speech and Drama', 'Arts'),
    ('Sports / Movement Science', 'Skills'),
    ('Sports Fitness / Body Training', 'Skills'),
    ('Sports Studies', 'Skills'),
    ('Study Skills', 'Other'),
    ('Theatre Studies', 'Arts'),
    ('Theatrical Makeup', 'Skills'),
    ('Travel and Tourism', 'Skills'),
    ('Turkish', 'Humanities'),
    ('Untranslated Literature', 'Humanities'),
    ('Urdu', 'Humanities'),
    ('Vehicle Body Maintenance / Repair', 'Skills'),
    ('Vehicle Maintenance / Repair', 'Skills'),
    ('Visual Arts', 'Arts')
""")

# Then update the aggregations to use this table:
cursor.execute("""
    INSERT INTO ks5_enrollment_summary
    SELECT 
        urn,
        year,
        SUM(CASE WHEN number_exams = 'supp' THEN 1 ELSE CAST(number_exams AS INTEGER) END) AS total_entries
    FROM ks5_raw
    WHERE grade = 'Total'
    GROUP BY urn, year
""")

cursor.execute("""
    INSERT INTO ks5_grade_summary
    SELECT 
        urn,
        year,
        SUM(CASE 
            WHEN number_exams != 'supp' AND grade = '*' THEN CAST(number_exams AS INTEGER) * 6.0
            WHEN number_exams != 'supp' AND grade = 'A' THEN CAST(number_exams AS INTEGER) * 5.0
            WHEN number_exams != 'supp' AND grade = 'B' THEN CAST(number_exams AS INTEGER) * 4.0
            WHEN number_exams != 'supp' AND grade = 'C' THEN CAST(number_exams AS INTEGER) * 3.0
            WHEN number_exams != 'supp' AND grade = 'D' THEN CAST(number_exams AS INTEGER) * 2.0
            WHEN number_exams != 'supp' AND grade = 'E' THEN CAST(number_exams AS INTEGER) * 1.0
            ELSE 0 END) / 
            NULLIF(SUM(CASE WHEN number_exams != 'supp' THEN CAST(number_exams AS INTEGER) ELSE 0 END), 0) AS avg_grade,
        SUM(CASE WHEN s.category = 'STEM' AND number_exams != 'supp' THEN 
            CASE 
                WHEN grade = '*' THEN CAST(number_exams AS INTEGER) * 6.0
                WHEN grade = 'A' THEN CAST(number_exams AS INTEGER) * 5.0
                WHEN grade = 'B' THEN CAST(number_exams AS INTEGER) * 4.0
                WHEN grade = 'C' THEN CAST(number_exams AS INTEGER) * 3.0
                WHEN grade = 'D' THEN CAST(number_exams AS INTEGER) * 2.0
                WHEN grade = 'E' THEN CAST(number_exams AS INTEGER) * 1.0
                ELSE 0 END ELSE 0 END) / 
            NULLIF(SUM(CASE WHEN s.category = 'STEM' AND number_exams != 'supp' THEN CAST(number_exams AS INTEGER) ELSE 0 END), 0) AS stem_avg_grade,
        SUM(CASE WHEN s.category = 'Arts' AND number_exams != 'supp' THEN 
            CASE 
                WHEN grade = '*' THEN CAST(number_exams AS INTEGER) * 6.0
                WHEN grade = 'A' THEN CAST(number_exams AS INTEGER) * 5.0
                WHEN grade = 'B' THEN CAST(number_exams AS INTEGER) * 4.0
                WHEN grade = 'C' THEN CAST(number_exams AS INTEGER) * 3.0
                WHEN grade = 'D' THEN CAST(number_exams AS INTEGER) * 2.0
                WHEN grade = 'E' THEN CAST(number_exams AS INTEGER) * 1.0
                ELSE 0 END ELSE 0 END) / 
            NULLIF(SUM(CASE WHEN s.category = 'Arts' AND number_exams != 'supp' THEN CAST(number_exams AS INTEGER) ELSE 0 END), 0) AS arts_avg_grade,
        SUM(CASE WHEN s.category = 'Business & Economics' AND number_exams != 'supp' THEN 
            CASE 
                WHEN grade = '*' THEN CAST(number_exams AS INTEGER) * 6.0
                WHEN grade = 'A' THEN CAST(number_exams AS INTEGER) * 5.0
                WHEN grade = 'B' THEN CAST(number_exams AS INTEGER) * 4.0
                WHEN grade = 'C' THEN CAST(number_exams AS INTEGER) * 3.0
                WHEN grade = 'D' THEN CAST(number_exams AS INTEGER) * 2.0
                WHEN grade = 'E' THEN CAST(number_exams AS INTEGER) * 1.0
                ELSE 0 END ELSE 0 END) / 
            NULLIF(SUM(CASE WHEN s.category = 'Business & Economics' AND number_exams != 'supp' THEN CAST(number_exams AS INTEGER) ELSE 0 END), 0) AS business_economics_avg_grade
    FROM ks5_raw r
    LEFT JOIN subjects s ON r.subject = s.subject_name
    WHERE r.grade NOT IN ('Total', 'supp')
    AND r.number_exams != 'supp'
    AND r.number_exams IS NOT NULL  -- Handle any blanks
    AND s.subject_name IS NOT NULL  -- Ensure join matches
    GROUP BY urn, year
""")

conn.commit()
conn.close()
print("Aggregation complete!")