# ============================================
# PDF REPORT GENERATOR
# ============================================
# Generates professional printable PDF reports with patient info, predictions, and recommendations

import os
from datetime import datetime
from fpdf import FPDF


def generate_pdf_report(patient_info, prediction_result, recommendations, gradcam_path=None):
    """
    Generate a professional PDF report for the patient.
    
    Args:
        patient_info: Dictionary with patient details (name, email, age, gender)
        prediction_result: Dictionary with prediction details (prediction, confidence, title)
        recommendations: Dictionary with recommendations
        gradcam_path: Path to Grad-CAM image (optional)
    
    Returns:
        Path to generated PDF file
    """
    pdf = PDF()
    pdf.add_page()
    
    # ============================================
    # HEADER
    # ============================================
    pdf.set_fill_color(30, 60, 114)  # Dark blue
    pdf.rect(0, 0, 210, 35, 'F')
    
    pdf.set_font("Arial", "B", 24)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 25, "Liver Disease Detection Report", 0, 1, "C")
    
    pdf.set_font("Arial", "I", 10)
    pdf.set_text_color(200, 200, 200)
    pdf.cell(0, 5, "AI-Powered Liver Health Assessment", 0, 1, "C")
    
    pdf.ln(15)
    
    # Report Date and ID
    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(100, 100, 100)
    report_id = f"Report ID: LD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    pdf.cell(0, 8, report_id, 0, 1, "L")
    pdf.cell(0, 8, f"Date: {datetime.now().strftime('%B %d, %Y')}", 0, 1, "L")
    pdf.ln(10)
    
    # ============================================
    # PATIENT INFORMATION
    # ============================================
    pdf.set_fill_color(240, 248, 255)
    pdf.rect(10, pdf.get_y(), 190, 8, 'F')
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(30, 60, 114)
    pdf.cell(0, 8, "PATIENT INFORMATION", 0, 1)
    pdf.ln(3)
    
    pdf.set_font("Arial", "", 11)
    pdf.set_text_color(60, 60, 60)
    
    # Two column layout for patient info
    pdf.cell(50, 8, f"Name: {patient_info.get('name', 'N/A')}", 0, 0)
    pdf.cell(50, 8, f"Age: {patient_info.get('age', 'N/A')}", 0, 1)
    pdf.cell(50, 8, f"Gender: {patient_info.get('gender', 'N/A')}", 0, 0)
    pdf.cell(50, 8, f"Email: {patient_info.get('email', 'N/A')}", 0, 1)
    
    pdf.ln(10)
    
    # ============================================
    # DIAGNOSIS RESULTS
    # ============================================
    pdf.set_fill_color(240, 248, 255)
    pdf.rect(10, pdf.get_y(), 190, 8, 'F')
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(30, 60, 114)
    pdf.cell(0, 8, "DIAGNOSIS RESULTS", 0, 1)
    pdf.ln(3)
    
    # Determine status
    is_healthy = prediction_result.get("prediction") == "Healthy"
    
    # Diagnosis box
    if is_healthy:
        pdf.set_fill_color(212, 237, 218)  # Light green
        pdf.set_text_color(21, 87, 36)  # Dark green
    else:
        pdf.set_fill_color(248, 215, 218)  # Light red
        pdf.set_text_color(114, 28, 36)  # Dark red
    
    pdf.rect(10, pdf.get_y(), 190, 25, 'F')
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"DIAGNOSIS: {prediction_result.get('prediction', 'N/A').upper()}", 0, 1, "C")
    
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Confidence Level: {prediction_result.get('confidence', 'N/A')}%", 0, 1, "C")
    
    pdf.set_text_color(60, 60, 60)
    pdf.ln(5)
    
    # Add Grad-CAM image if available
    if gradcam_path and os.path.exists(gradcam_path):
        pdf.ln(10)
        pdf.set_font("Arial", "B", 12)
        pdf.set_text_color(30, 60, 114)
        pdf.cell(0, 10, "Grad-CAM Visualization (AI Attention Map)", 0, 1)
        
        try:
            # Calculate dimensions to fit nicely
            pdf.image(gradcam_path, x=55, w=100)
        except:
            pdf.set_font("Arial", "", 10)
            pdf.set_text_color(150, 150, 150)
            pdf.cell(0, 10, "[Image could not be displayed]", 0, 1)
    
    pdf.ln(10)
    
    # ============================================
    # RECOVERY STEPS / RECOMMENDATIONS
    # ============================================
    if recommendations:
        pdf.set_fill_color(240, 248, 255)
        pdf.rect(10, pdf.get_y(), 190, 8, 'F')
        pdf.set_font("Arial", "B", 12)
        pdf.set_text_color(30, 60, 114)
        
        section_title = "RECOVERY STEPS" if not is_healthy else "PREVENTIVE MEASURES"
        pdf.cell(0, 8, section_title, 0, 1)
        pdf.ln(3)
        
        pdf.set_text_color(60, 60, 60)
        pdf.set_font("Arial", "", 10)
        
        # Use recovery_steps if available, otherwise use do/dont
        steps = recommendations.get('recovery_steps', [])
        
        if steps:
            for i, step in enumerate(steps, 1):
                # Check if we need a new page
                if pdf.get_y() > 240:
                    pdf.add_page()
                    pdf.ln(5)
                
                pdf.set_font("Arial", "B", 10)
                pdf.cell(12, 6, f"{i}.", 0, 0)
                pdf.set_font("Arial", "", 10)
                pdf.multi_cell(0, 6, step)
                pdf.ln(2)
        
        pdf.ln(10)
        
        # ============================================
        # DIET RECOMMENDATIONS
        # ============================================
        pdf.set_fill_color(240, 248, 255)
        pdf.rect(10, pdf.get_y(), 190, 8, 'F')
        pdf.set_font("Arial", "B", 12)
        pdf.set_text_color(30, 60, 114)
        pdf.cell(0, 8, "DIET RECOMMENDATIONS", 0, 1)
        pdf.ln(3)
        
        pdf.set_text_color(60, 60, 60)
        
        # Foods to EAT
        pdf.set_font("Arial", "B", 11)
        pdf.set_text_color(40, 167, 69)  # Green
        pdf.cell(0, 8, "Foods to INCLUDE:", 0, 1)
        
        pdf.set_font("Arial", "", 10)
        pdf.set_text_color(60, 60, 60)
        
        if recommendations.get("diet") and recommendations["diet"].get("foods_to_eat"):
            foods = recommendations["diet"]["foods_to_eat"]
            for food in foods:
                pdf.cell(10, 6, chr(149), 0, 0)
                pdf.cell(0, 6, food, 0, 1)
        
        pdf.ln(5)
        
        # Foods to AVOID
        pdf.set_font("Arial", "B", 11)
        pdf.set_text_color(220, 53, 69)  # Red
        pdf.cell(0, 8, "Foods to AVOID:", 0, 1)
        
        pdf.set_font("Arial", "", 10)
        pdf.set_text_color(60, 60, 60)
        
        if recommendations.get("diet") and recommendations["diet"].get("foods_to_avoid"):
            foods = recommendations["diet"]["foods_to_avoid"]
            for food in foods:
                pdf.cell(10, 6, chr(149), 0, 0)
                pdf.cell(0, 6, food, 0, 1)
        
        pdf.ln(5)
        
        # Meal Tips
        if recommendations.get("diet") and recommendations["diet"].get("meal_tips"):
            pdf.ln(5)
            pdf.set_fill_color(255, 243, 205)  # Light yellow
            pdf.rect(10, pdf.get_y(), 190, 6, 'F')
            pdf.set_font("Arial", "B", 11)
            pdf.set_text_color(133, 100, 4)  # Yellow-brown
            pdf.cell(0, 8, "Meal Tips:", 0, 1)
            
            pdf.set_font("Arial", "", 10)
            pdf.set_text_color(60, 60, 60)
            
            for tip in recommendations["diet"]["meal_tips"]:
                pdf.cell(10, 6, chr(149), 0, 0)
                pdf.cell(0, 6, tip, 0, 1)
        
        pdf.ln(10)
        
        # ============================================
        # FOLLOW-UP RECOMMENDATIONS
        # ============================================
        pdf.set_fill_color(231, 243, 255)  # Light blue
        pdf.rect(10, pdf.get_y(), 190, 8, 'F')
        pdf.set_font("Arial", "B", 12)
        pdf.set_text_color(0, 86, 179)  # Blue
        pdf.cell(0, 8, "FOLLOW-UP RECOMMENDATIONS", 0, 1)
        pdf.ln(3)
        
        pdf.set_font("Arial", "", 10)
        pdf.set_text_color(60, 60, 60)
        
        if recommendations.get("follow_up"):
            pdf.multi_cell(0, 6, f"Next Steps: {recommendations['follow_up']}")
            pdf.ln(3)
        
        if recommendations.get("recovery_time"):
            if is_healthy:
                pdf.set_font("Arial", "B", 11)
                pdf.cell(0, 8, "Maintain healthy lifestyle for life-long wellness.", 0, 1)
            else:
                pdf.set_font("Arial", "B", 11)
                pdf.cell(0, 8, f"Expected Recovery Time: {recommendations['recovery_time']}", 0, 1)
    
    # ============================================
    # FOOTER
    # ============================================
    pdf.ln(20)
    pdf.set_draw_color(200, 200, 200)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font("Arial", "I", 9)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 6, "This report is generated by the Liver Disease Detection AI System.", 0, 1, "C")
    pdf.cell(0, 6, "This is an automated assessment and should be reviewed by a healthcare professional.", 0, 1, "C")
    pdf.cell(0, 6, "For medical advice, please consult with a qualified hepatologist or liver specialist.", 0, 1, "C")
    
    # Save PDF
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static", "reports")
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"liver_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(output_dir, filename)
    pdf.output(filepath)
    
    return filepath


# Custom PDF Class
class PDF(FPDF):
    def header(self):
        pass  # Custom header handled in generate_pdf_report
    
    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

