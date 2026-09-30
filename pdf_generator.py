from fpdf import FPDF
import datetime

def generate_duty_leave_pdf(student_name: str, event_name: str, actual_missed: dict, simulation_results: dict) -> str:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Header
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="DUTY LEAVE APPLICATION", ln=True, align='C')
    pdf.ln(10)
    
    # Body
    pdf.set_font("Arial", size=12)
    date_today = datetime.date.today().strftime("%B %d, %Y")
    pdf.cell(200, 10, txt=f"Date: {date_today}", ln=True)
    pdf.ln(5)
    
    pdf.multi_cell(0, 10, txt=f"This is to formally request duty leave for {student_name} to participate in the {event_name}. Below is the breakdown of affected classes and the mathematically forecasted attendance upon return.")
    pdf.ln(5)
    
    # Missed Classes Section
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Classes to be missed:", ln=True)
    pdf.set_font("Arial", size=12)
    for sub, count in actual_missed.items():
        pdf.cell(200, 10, txt=f"- {sub}: {count} classes", ln=True)
        
    pdf.ln(5)
    
    # Post-Event Standing Section
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Attendance Verification (Post-Event):", ln=True)
    pdf.set_font("Arial", size=12)
    for sub, data in simulation_results.items():
        status = "Safe" if data['is_safe'] else f"WARNING (Needs {data['recovery_classes_needed']} classes to recover)"
        pdf.cell(200, 10, txt=f"- {sub}: {data['projected_percent']:.2f}% ({status})", ln=True)
        
    pdf.ln(20)
    pdf.cell(200, 10, txt="Student Signature: ___________________", ln=True)
    pdf.cell(200, 10, txt="HOD Signature:     ___________________", ln=True)
    
    # Save the file locally
    filename = f"Duty_Leave_{event_name.replace(' ', '_')}.pdf"
    pdf.output(filename)
    return filename