#!/usr/bin/env python3
# Clear ALL other Lalitha/Padhmavathi records except the example.com ones with single grades

import sqlite3
from patient_history import DB_PATH

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Protect the desired ones
protected = [4, 5]  # Lalitha@example.com ID4 Grade_1 only, Padmavathi@example.com ID5 Grade_2 only

print("=== CLEANING OLD RECORDS ===")

# Get all patients with similar names
cursor.execute("""
    SELECT id, name, email FROM patients 
    WHERE LOWER(name) LIKE '%lalitha%' OR LOWER(name) LIKE '%padma%'
""")
targets = cursor.fetchall()
print("Target patients:", targets)

for pat in targets:
    pat_id = pat[0]
    if pat_id in protected:
        print(f"PROTECTED: {pat[1]} ({pat[2]})")
        continue
    
    # Delete predictions
    cursor.execute("DELETE FROM biomedical_data WHERE prediction_id IN (SELECT id FROM predictions WHERE patient_id = ?)", (pat_id,))
    del_preds = cursor.execute("DELETE FROM predictions WHERE patient_id = ?", (pat_id,)).rowcount
    print(f"Deleted {del_preds} predictions for {pat[1]} ({pat[2]})")
    
    # Optional: delete patient if no other data
    # cursor.execute("DELETE FROM patients WHERE id = ?", (pat_id,))

conn.commit()
conn.close()

print("\n=== POST-CLEAN VERIFICATION ===")
exec(open('scripts/full_db_check.py').read())

print("\n✅ Clean complete. Now ONLY example.com have single correct grades.")
