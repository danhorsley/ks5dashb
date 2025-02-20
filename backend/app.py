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

@app.get("/schools/{urn}")
def get_school(urn: str):
    conn = sqlite3.connect("C:/Users/eden_/OneDrive/Desktop/ks5dashb/schools.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT year, total_entries, avg_grade, stem_avg_grade, arts_avg_grade 
        FROM ks5_school_summary 
        WHERE urn = ? 
        ORDER BY year
    """, (urn,))
    data = [{"year": r[0], "entries": r[1], "avg_grade": r[2], "stem": r[3], "arts": r[4]} for r in cursor.fetchall()]
    conn.close()
    return {"school": urn, "data": data}