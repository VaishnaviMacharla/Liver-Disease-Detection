#!/usr/bin/env python3
# FINAL CLEAN: Remove ALL non-example.com Lalitha/Padhmavathi predictions/patients

import sqlite3
from patient_history import DB_PATH

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("=== FINAL CLEAN ===")

# Target exact name matches excluding example.com
cursor.execute("""
    DELETE FROM biomedical_data WHERE prediction_id IN (
        SELECT p.id FROM predictions p 
        JOIN patients pa ON p.patient_id = pa.id 
        WHERE (LOWER(pa.name) LIKE '%lalitha%' OR LOWER(pa.name) LIKE '%padhma%') 
        AND pa.email NOT LIKE '%example.com'
    )
""")
print(f"Deleted {cursor.rowcount} biomedical records")

cursor.execute("""
    DELETE FROM predictions WHERE patient_id IN (
        SELECT pa.id FROM patients pa 
        WHERE (LOWER(pa.name) LIKE '%lalitha%' OR LOWER(pa.name) LIKE '%padhma%') 
        AND pa.email NOT LIKE '%example.com'
    )
""")
print(f"Deleted {cursor.rowcount} prediction records")

# Delete empty patients
cursor.execute("""
    DELETE FROM patients WHERE id NOT IN (
        SELECT DISTINCT patient_id FROM predictions
    ) AND (LOWER(name) LIKE '%lalitha%' OR LOWER(name) LIKE '%padhma%')
""")
print(f"Deleted {cursor.rowcount} empty patients")

conn.commit()
conn.close()

print("\n=== VERIFICATION ===")
exec(open('scripts/full_db_check.py').read())

print("\n✅ NOW: Use ONLY lalitha@example.com (Grade_1) & padmavathi@example.com (Grade_2)")
