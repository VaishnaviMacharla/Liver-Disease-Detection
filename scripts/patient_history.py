# ============================================
# PATIENT HISTORY DATABASE
# ============================================
# SQLite database for tracking patient predictions over time

import sqlite3
import os
from datetime import datetime

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, "patient_history.db")


def init_database():
    """Initialize the SQLite database with required tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create patients table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            phone TEXT,
            age INTEGER,
            gender TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create predictions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            prediction TEXT NOT NULL,
            confidence REAL NOT NULL,
            image_path TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    ''')
    
    # Create biomedical_data table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS biomedical_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prediction_id INTEGER,
            total_bilirubin REAL,
            direct_bilirubin REAL,
            alk_phosphate REAL,
            alt REAL,
            ast REAL,
            proteins REAL,
            albumin REAL,
            ratio REAL,
            FOREIGN KEY (prediction_id) REFERENCES predictions (id)
        )
    ''')
    
    conn.commit()
    conn.close()


def add_patient(name, email=None, phone=None, age=None, gender=None):
    """Add a new patient to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO patients (name, email, phone, age, gender)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, email, phone, age, gender))
        
        patient_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return patient_id
    except sqlite3.IntegrityError:
        conn.close()
        # Return existing patient ID
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM patients WHERE email = ?', (email,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None


def add_prediction(patient_id, prediction, confidence, image_path=None, notes=None,
                   total_bilirubin=None, direct_bilirubin=None, alk_phosphate=None,
                   alt=None, ast=None, proteins=None, albumin=None, ratio=None):
    """Add a new prediction record."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Insert prediction
    cursor.execute('''
        INSERT INTO predictions (patient_id, prediction, confidence, image_path, notes)
        VALUES (?, ?, ?, ?, ?)
    ''', (patient_id, prediction, confidence, image_path, notes))
    
    prediction_id = cursor.lastrowid
    
    # Insert biomedical data
    cursor.execute('''
        INSERT INTO biomedical_data (
            prediction_id, total_bilirubin, direct_bilirubin, alk_phosphate,
            alt, ast, proteins, albumin, ratio
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (prediction_id, total_bilirubin, direct_bilirubin, alk_phosphate,
          alt, ast, proteins, albumin, ratio))
    
    conn.commit()
    conn.close()
    
    return prediction_id


def get_patient_history(patient_id):
    """Get all predictions for a specific patient."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get patient info
    cursor.execute('SELECT * FROM patients WHERE id = ?', (patient_id,))
    patient = cursor.fetchone()
    
    # Get all predictions with biomedical data
    cursor.execute('''
        SELECT p.*, b.total_bilirubin, b.direct_bilirubin, b.alk_phosphate,
               b.alt, b.ast, b.proteins, b.albumin, b.ratio
        FROM predictions p
        LEFT JOIN biomedical_data b ON p.id = b.prediction_id
        WHERE p.patient_id = ?
        ORDER BY p.created_at DESC
    ''', (patient_id,))
    
    predictions = cursor.fetchall()
    conn.close()
    
    return {
        'patient': dict(patient) if patient else None,
        'predictions': [dict(p) for p in predictions]
    }


def get_patient_by_email(email):
    """Get patient by email."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM patients WHERE email = ?', (email,))
    patient = cursor.fetchone()
    conn.close()
    
    return dict(patient) if patient else None


def get_patient_by_id(patient_id):
    """Get patient by ID."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM patients WHERE id = ?', (patient_id,))
    patient = cursor.fetchone()
    conn.close()
    
    return dict(patient) if patient else None


def get_all_patients():
    """Get all patients."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM patients ORDER BY created_at DESC')
    patients = cursor.fetchall()
    conn.close()
    
    return [dict(p) for p in patients]


def get_latest_prediction(patient_id):
    """Get the most recent prediction for a patient."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM predictions
        WHERE patient_id = ?
        ORDER BY created_at DESC
        LIMIT 1
    ''', (patient_id,))
    
    prediction = cursor.fetchone()
    conn.close()
    
    return dict(prediction) if prediction else None


def format_history_html(patient_id):
    """Format patient history as HTML."""
    history = get_patient_history(patient_id)
    
    if not history['patient']:
        return "<p>No patient found.</p>"
    
    patient = history['patient']
    predictions = history['predictions']
    
    html = f"""
    <div class="patient-history">
        <div class="patient-info">
            <h2>Patient: {patient['name']}</h2>
            <p><strong>Email:</strong> {patient['email'] or 'N/A'}</p>
            <p><strong>Phone:</strong> {patient['phone'] or 'N/A'}</p>
            <p><strong>Age:</strong> {patient['age'] or 'N/A'}</p>
            <p><strong>Member Since:</strong> {patient['created_at']}</p>
        </div>
        
        <div class="predictions-list">
            <h3>Prediction History ({len(predictions)} records)</h3>
    """
    
    if not predictions:
        html += "<p>No predictions yet.</p>"
    else:
        for i, pred in enumerate(predictions, 1):
            status_class = "healthy" if pred['prediction'] == 'Healthy' else "disease"
            status_icon = "✅" if pred['prediction'] == 'Healthy' else "⚠️"
            
            html += f"""
            <div class="prediction-card {status_class}">
                <div class="prediction-header">
                    <span class="prediction-number">#{i}</span>
                    <span class="prediction-date">{pred['created_at']}</span>
                </div>
                <div class="prediction-result">
                    <strong>{status_icon} {pred['prediction']}</strong>
                    <span>Confidence: {pred['confidence']}%</span>
                </div>
            """
            
            # Add biomedical data if available
            if pred.get('total_bilirubin'):
                html += f"""
                <div class="biomedical-data">
                    <h4>Biomedical Test Results:</h4>
                    <div class="biomedical-grid">
                        <span>Total Bilirubin: {pred['total_bilirubin']} mg/dL</span>
                        <span>Direct Bilirubin: {pred['direct_bilirubin']} mg/dL</span>
                        <span>Alkaline Phosphate: {pred['alk_phosphate']} U/L</span>
                        <span>ALT: {pred['alt']} U/L</span>
                        <span>AST: {pred['ast']} U/L</span>
                        <span>Total Proteins: {pred['proteins']} g/dL</span>
                        <span>Albumin: {pred['albumin']} g/dL</span>
                        <span>A:G Ratio: {pred['ratio']}</span>
                    </div>
                </div>
                """
            
            if pred.get('notes'):
                html += f"<div class='notes'><strong>Notes:</strong> {pred['notes']}</div>"
            
            html += "</div>"
    
    html += """
        </div>
    </div>
    """
    
    return html


# Initialize database on import
init_database()

