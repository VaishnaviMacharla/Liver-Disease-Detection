#!/usr/bin/env python3
# Seed patient history DB with specific Lalitha (Grade_1 only) & Padmavathi (Grade_2 only)

import sqlite3
import os
from datetime import datetime, timedelta
from patient_history import DB_PATH, add_patient, add_prediction, get_patient_by_email, get_patient_history

print("=== Liver Disease Demo Data Seeder ===")

def clear_patient_predictions(email):
    """Clear all predictions for a patient."""
    patient = get_patient_by_email(email)
    if not patient:
        print(f"No patient {email}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM biomedical_data WHERE prediction_id IN (SELECT id FROM predictions WHERE patient_id = ?)", (patient['id'],))
    cursor.execute("DELETE FROM predictions WHERE patient_id = ?", (patient['id'],))
    conn.commit()
    conn.close()
    print(f"Cleared predictions for {email}")

def seed_lalitha():
    print("\n1. Seeding Lalitha (Grade_1 only)...")
    clear_patient_predictions("lalitha@example.com")
    patient_id = add_patient("Lalitha", "lalitha@example.com", age=45, gender="F")
    
    # Single Grade_1 prediction (older date)
    add_prediction(
        patient_id=patient_id,
        prediction="Grade_1",
        confidence=92.5,
        image_path="lalitha_grade1.jpg",  # Generic
        notes="Mild fatty liver detected",
        total_bilirubin=1.2,
        direct_bilirubin=0.3,
        alk_phosphate=120,
        alt=55,
        ast=60,
        proteins=7.2,
        albumin=4.1,
        ratio=1.76
    )
    print("Lalitha: 1x Grade_1 seeded")

def seed_padmavathi():
    print("\n2. Seeding Padmavathi (Grade_2 only)...")
    clear_patient_predictions("padmavathi@example.com")
    patient_id = add_patient("Padmavathi", "padmavathi@example.com", age=52, gender="F")
    
    # Single Grade_2 prediction (recent)
    add_prediction(
        patient_id=patient_id,
        prediction="Grade_2",
        confidence=88.7,
        image_path="padmavathi_grade2.jpg",
        notes="Moderate fatty liver",
        total_bilirubin=1.8,
        direct_bilirubin=0.6,
        alk_phosphate=180,
        alt=95,
        ast=110,
        proteins=6.8,
        albumin=3.7,
        ratio=1.46
    )
    print("Padmavathi: 1x Grade_2 seeded")

if __name__ == "__main__":
    seed_lalitha()
    seed_padmavathi()
    
    # Verify
    print("\n=== VERIFICATION ===")
    lalitha_history = get_patient_history(add_patient("Lalitha", "lalitha@example.com"))
    pad_history = get_patient_history(add_patient("Padmavathi", "padmavathi@example.com"))
    print(f"Lalitha predictions: {len(lalitha_history['predictions'])}")
    print(f"Padmavathi predictions: {len(pad_history['predictions'])}")
    if lalitha_history['predictions']:
        print(f"Lalitha latest: {lalitha_history['predictions'][0]['prediction']}")
    if pad_history['predictions']:
        print(f"Padmavathi latest: {pad_history['predictions'][0]['prediction']}")
    print("Seeding complete! Test: python scripts/app.py then /history with emails.")
