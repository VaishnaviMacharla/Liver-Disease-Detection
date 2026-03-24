#!/usr/bin/env python3
# Full DB inspection to diagnose issue

import sqlite3
from patient_history import DB_PATH

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("=== FULL PATIENTS LIST ===")
cursor.execute("SELECT id, name, email FROM patients ORDER BY name")
patients = cursor.fetchall()
for p in patients:
    print(f"ID {p[0]}: {p[1]} ({p[2]})")

print("\n=== ALL PREDICTIONS ===")
cursor.execute("""
    SELECT pa.name, pa.email, p.prediction, COUNT(*) as count 
    FROM predictions p 
    JOIN patients pa ON p.patient_id = pa.id 
    GROUP BY pa.id, pa.name, pa.email, p.prediction 
    ORDER BY pa.name
""")
preds = cursor.fetchall()
for pr in preds:
    print(f"{pr[0]} ({pr[1]}): {pr[2]} x{pr[3]}")

print("\n=== TOTAL PER PATIENT ===")
cursor.execute("""
    SELECT pa.id, pa.name, pa.email, COUNT(p.id) as total_preds 
    FROM patients pa 
    LEFT JOIN predictions p ON pa.id = p.patient_id 
    GROUP BY pa.id 
    ORDER BY total_preds DESC
""")
totals = cursor.fetchall()
for t in totals:
    print(f"ID {t[0]} {t[1]}: {t[3]} total predictions")

conn.close()
print("\nRun complete. Check for other Lalitha/Padmavathi variants.")
