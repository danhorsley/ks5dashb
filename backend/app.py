from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
def search_schools(q: str):
    print(f"Searching for: {q}")  # Debug: Log the query
    conn = sqlite3.connect("C:/Users/eden_/OneDrive/Desktop/ks5dashb/schools.db")
    cursor = conn.cursor()
    # Enhanced search: split query into words, case-insensitive, trim spaces
    words = [word.strip() for word in q.lower().split()]
    conditions = " OR ".join([f"LOWER(TRIM(school_name)) LIKE ?" for _ in words] + [f"LOWER(TRIM(urn)) LIKE ?"])
    params = [f"%{word}%" for word in words] + [f"%{q.lower()}%"]
    try:
        cursor.execute(f"""
            SELECT urn, school_name, local_authority, school_type 
            FROM schools 
            WHERE {conditions}
            LIMIT 10
        """, params)
        results = [{"urn": r[0], "name": r[1], "la": r[2], "type": r[3]} for r in cursor.fetchall()]
        print(f"Found results: {results}")  # Debug: Log results
    except Exception as e:
        print(f"Error in query: {e}")  # Debug: Log errors
        results = []
    finally:
        conn.close()
    return {"data": results}

@app.get("/schools/{urn}")
def get_school(urn: str):
    conn = sqlite3.connect("C:/Users/eden_/OneDrive/Desktop/ks5dashb/schools.db")
    cursor = conn.cursor()
    # Cast urn to INTEGER for enrollment_outcomes join, include total_employment
    cursor.execute("""
        SELECT e.year, e.total_entries, g.avg_grade, g.stem_avg_grade, g.arts_avg_grade, g.econ_avg_grade, g.humanities_avg_grade, o.total_cohort, o.total_employment, 
               s.school_name, s.local_authority, s.school_type, s.age_low, s.age_high
        FROM ks5_enrollment_summary e
        LEFT JOIN ks5_grade_summary g ON e.urn = g.urn AND e.year = g.year
        LEFT JOIN enrollment_outcomes o ON CAST(e.urn AS INTEGER) = o.urn AND e.year = o.year  -- Cast text urn to INTEGER
        LEFT JOIN schools s ON e.urn = s.urn
        WHERE e.urn = ? 
        ORDER BY e.year
    """, (urn.strip(),))
    data = [{"year": r[0], "entries": r[1], "avg_grade": float(r[2]) if r[2] else 0, "stem": float(r[3]) if r[3] else 0, "arts": float(r[4]) if r[4] else 0, "econ": float(r[5]) if r[5] else 0, "humanities": float(r[6]) if r[6] else 0, "cohort": r[7], "employment": r[8], "school": r[9], "la": r[10], "type": r[11], "min_age": r[12], "max_age": r[13]} for r in cursor.fetchall()]
    conn.close()
    # Find latest data (2024 or most recent), handle null values
    latest_data = next((d for d in data if d["year"] == 2024), data[-1] if data else {})
    cohort = latest_data.get("cohort") if latest_data.get("cohort") is not None else None
    employment = latest_data.get("employment") if latest_data.get("employment") is not None else None
    # Calculate staff_student_ratio with try/except, using employment as staff
    try:
        staff_student_ratio = cohort / employment if cohort is not None and employment is not None and employment != 0 else "N/A"
    except (TypeError, ZeroDivisionError):
        staff_student_ratio = "N/A"
    # Update data with employment and staff_student_ratio for the latest year
    for d in data:
        if d["year"] == latest_data["year"]:
            d["staff_student_ratio"] = str(staff_student_ratio) if staff_student_ratio != "N/A" else "N/A"
            d["employment"] = employment if employment is not None else "N/A"
    return {
        "school": urn,
        "data": data,
        "num_students": cohort if cohort is not None else "N/A",
        "num_staff": employment if employment is not None else "N/A",  # Use employment as staff
        "staff_student_ratio": str(staff_student_ratio) if staff_student_ratio != "N/A" else "N/A"
    }

@app.get("/national-averages")
def get_national_averages():
    conn = sqlite3.connect("C:/Users/eden_/OneDrive/Desktop/ks5dashb/schools.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT year, AVG(avg_grade) AS avg_grade, 
               AVG(stem_avg_grade) AS stem_avg, 
               AVG(arts_avg_grade) AS arts_avg, 
               AVG(econ_avg_grade) AS econ_avg,
               AVG(humanities_avg_grade) AS humanities_avg
        FROM ks5_grade_summary
        GROUP BY year
        ORDER BY year
    """)
    data = [{"year": r[0], "avg_grade": float(r[1]) if r[1] else 0, "stem": float(r[2]) if r[2] else 0, "arts": float(r[3]) if r[3] else 0, "econ": float(r[4]) if r[4] else 0, "humanities": float(r[5]) if r[5] else 0} for r in cursor.fetchall()]
    conn.close()
    return {"data": data}

@app.get("/regional-averages/{region}")
def get_regional_averages(region: str):
    conn = sqlite3.connect("C:/Users/eden_/OneDrive/Desktop/ks5dashb/schools.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT g.year, AVG(g.avg_grade) AS avg_grade, 
               AVG(g.stem_avg_grade) AS stem_avg, 
               AVG(g.arts_avg_grade) AS arts_avg, 
               AVG(g.econ_avg_grade) AS econ_avg,
               AVG(g.humanities_avg_grade) AS humanities_avg
        FROM ks5_grade_summary g
        JOIN schools s ON g.urn = s.urn
        WHERE s.region = ?
        GROUP BY g.year
        ORDER BY g.year
    """, (region,))
    data = [{"year": r[0], "avg_grade": float(r[1]) if r[1] else 0, "stem": float(r[2]) if r[2] else 0, "arts": float(r[3]) if r[3] else 0, "econ": float(r[4]) if r[4] else 0, "humanities": float(r[5]) if r[5] else 0} for r in cursor.fetchall()]
    conn.close()
    return {"region": region, "data": data}