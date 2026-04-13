import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from werkzeug.utils import secure_filename
from predict_with_gradcam_fixed import predict_image
from patient_history import add_patient, add_prediction, get_patient_by_email, get_patient_history, get_patient_by_id, format_history_html, init_database
from recommendations import get_recommendations
from report_generator import generate_pdf_report

# ==============================
# PATH SETUP
# ==============================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

STATIC_FOLDER = os.path.join(PROJECT_ROOT, "static")
TEMPLATE_FOLDER = os.path.join(PROJECT_ROOT, "templates")

app = Flask(__name__,
            static_folder=STATIC_FOLDER,
            template_folder=TEMPLATE_FOLDER)

# Secret key for sessions
app.secret_key = os.urandom(24)

UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ==============================
# ROUTES
# ==============================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/information")
def information_page():
    return render_template("information.html")

@app.route("/test")
def test_page():
    # Check if user is registered (patient_id in session)
    if 'patient_id' not in session:
        flash("Please register or login first to access the test page.", "error")
        return redirect(url_for("register_patient"))
    return render_template("test.html")

@app.route("/predict", methods=["POST"])
def predict():

    if "image" not in request.files:
        return "No file uploaded"

    file = request.files["image"]

    if file.filename == "":
        return "No file selected"

    # Secure filename + unique name
    filename = secure_filename(file.filename)
    unique_name = f"{uuid.uuid4().hex}_{filename}"
    filepath = os.path.join(UPLOAD_FOLDER, unique_name)
    file.save(filepath)

    result = predict_image(filepath)

    # ✅ Cap confidence at 99.99% (avoid unrealistic 100%)
    if result["confidence"] >= 100:
        result["confidence"] = 99.99

    # Get patient info from form (optional)
    patient_email = request.form.get("patient_email")
    patient_name = request.form.get("patient_name")
    patient_age = request.form.get("patient_age")
    
    # Save to patient history if patient info provided
    if patient_email or patient_name:
        # Get or create patient
        patient = get_patient_by_email(patient_email) if patient_email else None
        if not patient and patient_name:
            patient_id = add_patient(
                name=patient_name,
                email=patient_email,
                age=int(patient_age) if patient_age else None
            )
        elif patient:
            patient_id = patient['id']
        else:
            patient_id = None
        
        if patient_id:
            # Get biomedical data from form
            total_bilirubin = request.form.get("total_bilirubin")
            direct_bilirubin = request.form.get("direct_bilirubin")
            alk_phosphate = request.form.get("alk_phosphate")
            alt = request.form.get("alt")
            ast = request.form.get("ast")
            proteins = request.form.get("proteins")
            albumin = request.form.get("albumin")
            ratio = request.form.get("ratio")
            
            # Save prediction to history
            add_prediction(
                patient_id=patient_id,
                prediction=result["prediction"],
                confidence=result["confidence"],
                image_path=unique_name,
                total_bilirubin=float(total_bilirubin) if total_bilirubin else None,
                direct_bilirubin=float(direct_bilirubin) if direct_bilirubin else None,
                alk_phosphate=float(alk_phosphate) if alk_phosphate else None,
                alt=float(alt) if alt else None,
                ast=float(ast) if ast else None,
                proteins=float(proteins) if proteins else None,
                albumin=float(albumin) if albumin else None,
                ratio=float(ratio) if ratio else None
            )
            
            # Store patient_id in session
            session['patient_id'] = patient_id

    return render_template("result.html", result=result)


# ==============================
# PATIENT HISTORY ROUTES
# ==============================

@app.route("/register", methods=["GET", "POST"])
def register_patient():
    """Register a new patient."""
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        age = request.form.get("age")
        gender = request.form.get("gender")
        
        patient_id = add_patient(name=name, email=email, phone=phone, age=int(age) if age else None, gender=gender)
        session['patient_id'] = patient_id
        
        flash(f"Patient registered successfully! ID: {patient_id}", "success")
        return redirect(url_for("test_page"))
    
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login_patient():
    """Login an existing patient."""
    if request.method == "POST":
        email = request.form.get("email")
        
        patient = get_patient_by_email(email)
        if patient:
            session['patient_id'] = patient['id']
            flash(f"Welcome back, {patient['name']}!", "success")
            return redirect(url_for("test_page"))
        else:
            flash("No patient found with that email. Please register first.", "error")
    
    return redirect(url_for("register_patient"))


@app.route("/history", methods=["GET", "POST"])
def patient_history_page():
    """View patient history."""
    patient_id = session.get('patient_id')
    
    if request.method == "POST":
        email = request.form.get("email")
        patient = get_patient_by_email(email)
        if patient:
            patient_id = patient['id']
            session['patient_id'] = patient_id
        else:
            flash("No patient found with that email.", "error")
    
    if patient_id:
        history_html = format_history_html(patient_id)
        return render_template("history.html", history=history_html, patient_id=patient_id)
    
    return render_template("history.html", history=None, patient_id=None)


@app.route("/clear_history")
def clear_history():
    """Clear patient session."""
    session.pop('patient_id', None)
    flash("Session cleared.", "info")
    return redirect(url_for("home"))


@app.route("/download_report/<patient_id>")
def download_report(patient_id):
    """Generate and download PDF report for a patient."""
    patient_id = int(patient_id)
    
    # Get patient info
    patient = get_patient_by_id(patient_id)
    if not patient:
        flash("Patient not found.", "error")
        return redirect(url_for("home"))
    
    # Get latest prediction
    history = get_patient_history(patient_id)
    if not history['predictions']:
        flash("No predictions found for this patient.", "error")
        return redirect(url_for("patient_history_page"))
    
    # Get latest prediction
    prediction = history['predictions'][0]
    
    # Get recommendations
    recommendations = get_recommendations(prediction['prediction'])
    
    # Get Grad-CAM image path
    gradcam_path = None
    if prediction.get('image_path'):
        gradcam_full = os.path.join(STATIC_FOLDER, "uploads", prediction['image_path'])
        if os.path.exists(gradcam_full):
            gradcam_path = gradcam_full
    
    # Generate PDF
    pdf_path = generate_pdf_report(
        patient_info=patient,
        prediction_result=prediction,
        recommendations=recommendations,
        gradcam_path=gradcam_path
    )
    
    return send_file(pdf_path, as_attachment=True)

# ==============================
# RUN SERVER
# ==============================

if __name__ == "__main__":
    app.run(debug=True)