#!/usr/bin/env python3
# Optional: Minor enhancement to recommendations.py for person-name personalization

import re
from recommendations import get_recommendations

def personalize_recs(patient_name, disease_class):
    """Add patient name to recommendations (consistent core content)."""
    rec = get_recommendations(disease_class)
    
    # Prefix key steps with name (e.g. "Lalitha, follow low-fat...")
    if 'recovery_steps' in rec:
        rec['recovery_steps'] = [f"{patient_name}, {step}" for step in rec['recovery_steps']]
    
    rec['personalized_title'] = f"Personalized Plan for {patient_name}"
    rec['diet']['foods_to_eat'] = [f"{patient_name} should eat: {food}" for food in rec['diet']['foods_to_eat']]
    rec['diet']['foods_to_avoid'] = [f"{patient_name} should avoid: {food}" for food in rec['diet']['foods_to_avoid']]
    
    return rec

if __name__ == "__main__":
    # Demo
    print("Demo personalization (Grade_1 for Lalitha):")
    print(personalize_recs("Lalitha", "Grade_1")['recovery_steps'][:2])
    print("\nConsistent: Same every time.")
    print("To integrate: Modify app.py/report_generator.py to pass patient_name.")
