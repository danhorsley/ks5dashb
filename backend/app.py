# backend/app.py
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

@app.get("/schools")
def get_schools(urns: str):
    urn_list = urns.split(",")
    conn = sqlite3.connect("C:/Users/eden_/OneDrive/Desktop/ks5dashb/schools.db")
    cursor = conn.cursor()
    data = {}
    for urn in urn_list:
        cursor.execute("""
            SELECT e.year, e.total_entries, g.avg_grade, g.stem_avg_grade, g.arts_avg_grade, g.econ_avg_grade 
            FROM ks5_enrollment_summary e
            LEFT JOIN ks5_grade_summary g ON e.urn = g.urn AND e.year = g.year
            WHERE e.urn = ? 
            ORDER BY e.year
        """, (urn.strip(),))
        data[urn.strip()] = [{"year": r[0], "entries": r[1], "avg_grade": float(r[2]) if r[2] else 0, "stem": float(r[3]) if r[3] else 0, "arts": float(r[4]) if r[4] else 0, "econ": float(r[5]) if r[5] else 0} for r in cursor.fetchall()]
    conn.close()
    return data