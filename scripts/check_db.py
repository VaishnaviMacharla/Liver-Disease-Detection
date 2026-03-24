#!/usr/bin/env python3
# Verify DB content post-seeding

from patient_history import get_patient_by_email, get_patient_history, DB_PATH
import sqlite3

print("=== DB Verification ===")

# Check patients
conn = sqlite3.connect(DB_PATH)
cursor = sqlite3.connect(DB_PATH).cursor()
cursor.execute("SELECT name, email FROM patients WHERE email LIKE '%example.com'")
patients = cursor.fetchall()
print("Patients with example.com:")
for p in patients:
    print(f"  - {p[0]}: {p[1]}")

# Specific histories
lalitha = get_patient_by_email('lalitha@example.com')
pad = get_patient_by_email('padmavathi@example.com')

print(f"\nLalitha ({lalitha['id'] if lalitha else 'N/A'}): {len(get_patient_history(lalitha['id'] if lalitha else 0)['predictions'])} predictions")
if lalitha:
    preds = get_patient_history(lalitha['id'])['predictions']
    for p in preds:
        print(f"  Grade: {p['prediction']}")

print(f"\nPadmavathi ({pad['id'] if pad else 'N/A'}): {len(get_patient_history(pad['id'] if pad else 0)['predictions'])} predictions")
if pad:
    preds = get_patient_history(pad['id'])['predictions']
    for p in preds:
        print(f"  Grade: {p['prediction']}")

print("\nVerification complete.")
