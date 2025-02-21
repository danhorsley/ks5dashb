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

@app.get("/schools/{urn}")
def get_school(urn: str):
    conn = sqlite3.connect("C:/Users/eden_/OneDrive/Desktop/ks5dashb/schools.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT e.year, e.total_entries, g.avg_grade, g.stem_avg_grade, g.arts_avg_grade, g.econ_avg_grade, g.humanities_avg_grade, o.total_cohort, o.l3_cohort, 
           s.school_name, s.local_authority, s.school_type, s.age_low, s.age_high
    FROM ks5_enrollment_summary e
    LEFT JOIN ks5_grade_summary g ON e.urn = g.urn AND e.year = g.year
    LEFT JOIN enrollment_outcomes o ON e.urn = o.urn AND e.year = o.year
    LEFT JOIN schools s ON e.urn = s.urn
    WHERE e.urn = ? 
    ORDER BY e.year
    """, (urn.strip(),))
    data = [{"year": r[0], "entries": r[1], "avg_grade": float(r[2]) if r[2] else 0, "stem": float(r[3]) if r[3] else 0, "arts": float(r[4]) if r[4] else 0, "econ": float(r[5]) if r[5] else 0, "humanities": float(r[6]) if r[6] else 0, "cohort": r[7], "l3_cohort": r[8], "school": r[9], "la": r[10], "type": r[11], "min_age": r[12], "max_age": r[13]} for r in cursor.fetchall()]
    return {"school": urn, "data": data}
  

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
               AVG(g.econ_avg_grade) AS econ_avg
        FROM ks5_grade_summary g
        JOIN schools s ON g.urn = s.urn
        WHERE s.region = ?
        GROUP BY g.year
        ORDER BY g.year
    """, (region,))
    data = [{"year": r[0], "avg_grade": float(r[1]) if r[1] else 0, "stem": float(r[2]) if r[2] else 0, "arts": float(r[3]) if r[3] else 0, "econ": float(r[4]) if r[4] else 0} for r in cursor.fetchall()]
    conn.close()
    return {"region": region, "data": data}

@app.get("/schools/search")
def search_schools(q: str):
    conn = sqlite3.connect("C:/Users/eden_/OneDrive/Desktop/ks5dashb/schools.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT urn, school_name, local_authority, school_type 
        FROM schools 
        WHERE school_name LIKE ? OR urn LIKE ?
        LIMIT 10
    """, (f"%{q}%", f"%{q}%"))
    results = [{"urn": r[0], "name": r[1], "la": r[2], "type": r[3]} for r in cursor.fetchall()]
    conn.close()
    return results