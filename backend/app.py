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
    # Cast urn to INTEGER for enrollment_outcomes and gias_schools joins
    cursor.execute("""
        SELECT e.year, e.total_entries, g.avg_grade, g.stem_avg_grade, g.arts_avg_grade, g.econ_avg_grade, g.humanities_avg_grade, 
               COALESCE(o.total_cohort, gs.number_students) AS cohort,  -- Year 13 Size
               COALESCE(o.total_employment, gs.number_students) AS employment,  -- Num Staff (fallback to number_students if no employment)
               s.school_name, s.local_authority, s.school_type, s.age_low AS min_age, s.age_high AS max_age,
               gs.number_students AS total_school_students,  -- Total School Students
               gs.num_boys, gs.num_girls, gs.gender, gs.is_selective, gs.head, gs.website
        FROM ks5_enrollment_summary e
        LEFT JOIN ks5_grade_summary g ON e.urn = g.urn AND e.year = g.year
        LEFT JOIN enrollment_outcomes o ON CAST(e.urn AS INTEGER) = o.urn AND e.year = o.year
        LEFT JOIN gias_schools gs ON CAST(e.urn AS INTEGER) = gs.urn  -- Fallback for missing data
        LEFT JOIN schools s ON e.urn = s.urn
        WHERE e.urn = ? 
        ORDER BY e.year
    """, (urn.strip(),))
    data = [{"year": r[0], "entries": r[1], "avg_grade": float(r[2]) if r[2] else 0, "stem": float(r[3]) if r[3] else 0, "arts": float(r[4]) if r[4] else 0, "econ": float(r[5]) if r[5] else 0, "humanities": float(r[6]) if r[6] else 0, "year_13_size": r[7], "employment": r[8], "school": r[9], "la": r[10], "type": r[11], "min_age": r[12], "max_age": r[13], "total_school_students": r[14], "num_boys": r[15], "num_girls": r[16], "gender": r[17], "is_selective": r[18], "head": r[19], "website": r[20]} for r in cursor.fetchall()]
    conn.close()
    # Find latest data (2024 or most recent), handle null values
    latest_data = next((d for d in data if d["year"] == 2024), data[-1] if data else {})
    year_13_size = latest_data.get("year_13_size") if latest_data.get("year_13_size") is not None else None
    employment = latest_data.get("employment") if latest_data.get("employment") is not None else None
    total_school_students = latest_data.get("total_school_students") if latest_data.get("total_school_students") is not None else None
    num_boys = latest_data.get("num_boys") if latest_data.get("num_boys") is not None else None
    num_girls = latest_data.get("num_girls") if latest_data.get("num_girls") is not None else None
    gender = latest_data.get("gender") if latest_data.get("gender") is not None else None
    is_selective = latest_data.get("is_selective") if latest_data.get("is_selective") is not None else None
    head = latest_data.get("head") if latest_data.get("head") is not None else None
    website = latest_data.get("website") if latest_data.get("website") is not None else None
    # Calculate staff_student_ratio with try/except, using employment as staff
    try:
        staff_student_ratio = year_13_size / employment if year_13_size is not None and employment is not None and employment != 0 else "N/A"
    except (TypeError, ZeroDivisionError):
        staff_student_ratio = "N/A"
    # Update data with employment and staff_student_ratio for the latest year
    for d in data:
        if d["year"] == latest_data["year"]:
            d["staff_student_ratio"] = str(staff_student_ratio) if staff_student_ratio != "N/A" else "N/A"
            d["employment"] = employment if employment is not None else "N/A"
            d["total_school_students"] = total_school_students if total_school_students is not None else "N/A"
            d["num_boys"] = num_boys if num_boys is not None else "N/A"
            d["num_girls"] = num_girls if num_girls is not None else "N/A"
            d["gender"] = gender if gender is not None else "N/A"
            d["is_selective"] = is_selective if is_selective is not None else "N/A"
            d["head"] = head if head is not None else "N/A"
            d["website"] = website if website is not None else "N/A"
            d["year_13_size"] = year_13_size if year_13_size is not None else "N/A"
    return {
        "school": urn,
        "data": data,
        "year_13_size": year_13_size if year_13_size is not None else "N/A",  # Renamed from "cohort" to "year_13_size"
        "total_school_students": total_school_students if total_school_students is not None else "N/A",
        "employment": employment if employment is not None else "N/A",
        "num_staff": employment if employment is not None else "N/A",  # Use employment as staff
        "staff_student_ratio": str(staff_student_ratio) if staff_student_ratio != "N/A" else "N/A",
        "num_boys": num_boys if num_boys is not None else "N/A",
        "num_girls": num_girls if num_girls is not None else "N/A",
        "gender": gender if gender is not None else "N/A",
        "is_selective": is_selective if is_selective is not None else "N/A",
        "head": head if head is not None else "N/A",
        "website": website if website is not None else "N/A",
        "min_age": latest_data.get("min_age") if latest_data.get("min_age") is not None else "N/A",
        "max_age": latest_data.get("max_age") if latest_data.get("max_age") is not None else "N/A"
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