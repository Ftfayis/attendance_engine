import streamlit as st
import os
from models import Subject, LeaveEvent, RiskAnalyzer
from pdf_generator import generate_duty_leave_pdf
from ai_parser import extract_timetable_data

# MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(page_title="OptiLeave", page_icon="🎓", layout="wide")

if "analyzer" not in st.session_state:
    st.session_state.analyzer = RiskAnalyzer()
if "extracted_data" not in st.session_state:
    st.session_state.extracted_data = {}

# Hide Streamlit default styling for a cleaner look
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            /* Add a subtle glow to primary buttons */
            .stButton>button {
                border-radius: 8px;
                transition: all 0.3s ease;
            }
            .stButton>button:hover {
                box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
                border-color: #6366F1;
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("OptiLeave Dashboard")
st.markdown("Automated Academic Compliance & Risk Engine")
st.write("---")

# --- CREATE TABS ---
tab1, tab2, tab3 = st.tabs(["📊 Live Dashboard", "🤖 AI Auto-Import", "📄 Duty Leave Export"])


# ==========================================
# TAB 1: DASHBOARD & MANUAL OVERRIDES
# ==========================================
with tab1:
    st.subheader("Current Academic Standing")
    
    if st.session_state.analyzer.subjects:
        # Create a dynamic 3-column grid for metrics
        cols = st.columns(3)
        col_index = 0
        
        for name, sub in st.session_state.analyzer.subjects.items():
            with cols[col_index % 3]:
                st.metric(
                    label=name, 
                    value=f"{sub.get_current_percentage():.2f}%", 
                    delta=f"{sub.get_remaining_safe_cuts()} safe Hours left"
                )
            col_index += 1
    else:
        st.info("No subjects added yet. Go to the AI Auto-Import tab or add them below.")

    st.write("---")
    st.subheader("Update Subject Data")
    
    has_extracted = "extracted_data" in st.session_state and st.session_state.extracted_data

    with st.form("add_subject_form"):
        if has_extracted:
            options = list(st.session_state.extracted_data.keys()) + ["+ Type Custom Subject"]
            selected_option = st.selectbox("Choose Subject to Update", options)
            
            if selected_option == "+ Type Custom Subject":
                sub_name = st.text_input("Custom Subject Name")
            else:
                sub_name = selected_option
        else:
            sub_name = st.text_input("Subject Name")
            
        total_held = st.number_input("Total class Hours Held", min_value=0, step=1)
        attended = st.number_input("Classes hours Attended", min_value=0, step=1)
        submit_subject = st.form_submit_button("Calculate & Add")

        if submit_subject and sub_name:
            new_sub = Subject(sub_name, total_held, attended)
            st.session_state.analyzer.add_subject(new_sub)
            st.success(f"Updated attendance for {sub_name}!")
            st.rerun() 


# ==========================================
# TAB 2: AI AUTO-IMPORT
# ==========================================
with tab2:
    st.info("Securely extract subjects and hours directly from an image. Your API key is not saved.")
    api_key_input = st.text_input("Gemini API Key", type="password")
    uploaded_image = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
    
    if st.button("Extract Data"):
        if uploaded_image and api_key_input:
            with st.spinner("AI is analyzing your timetable..."):
                temp_path = "temp_image.jpg"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_image.getbuffer())
                
                data = extract_timetable_data(temp_path, api_key_input)
                
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                
                if "Error" in data:
                    st.error(data["Error"])
                else:
                    st.session_state.extracted_data = data
                    st.success("Extraction complete! Choose your subjects below.")
        else:
            st.warning("Please enter your API key and upload an image.")

    if st.session_state.extracted_data:
        st.write("---")
        st.subheader("Filter Your Subjects")
        available_subjects = list(st.session_state.extracted_data.keys())
        
        selected_subjects = st.multiselect(
            "Select which subjects you want to track on your dashboard right now:",
            options=available_subjects,
            default=available_subjects
        )
        
        if st.button("Apply Selection"):
            st.session_state.analyzer.subjects = {}
            
            for sub_name in selected_subjects:
                weekly_hours = st.session_state.extracted_data[sub_name]
                new_sub = Subject(sub_name, weekly_hours, weekly_hours)
                st.session_state.analyzer.add_subject(new_sub)
            
            st.success("Dashboard updated!")
            st.rerun()


# ==========================================
# TAB 3: SIMULATE & EXPORT PDF
# ==========================================
with tab3:
    if not st.session_state.analyzer.subjects:
        st.warning("Please add subjects in the Dashboard or AI Auto-Import tab first.")
    else:
        with st.form("simulate_leave_form"):
            event_name = st.text_input("Event Name ")
            student_name = st.text_input("Student Name ")
            
            st.write("Specify class hours you will miss in this subject:")
            missed_counts = {}
            for sub_name in st.session_state.analyzer.subjects.keys():
                missed_counts[sub_name] = st.number_input(f" {sub_name} class hours", min_value=0, step=1)
                
            submit_leave = st.form_submit_button("Run Risk Simulation")

        if submit_leave and event_name:
            actual_missed = {k: v for k, v in missed_counts.items() if v > 0}
            new_leave = LeaveEvent(event_name, actual_missed)
            st.session_state.analyzer.add_leave_event(new_leave)
            
            st.subheader("Simulation Results")
            results = st.session_state.analyzer.simulate_future_attendance()
            
            for sub, data in results.items():
                status_color = "green" if data["is_safe"] else "red"
                st.markdown(f"**{sub}**: Projected <span style='color:{status_color}'>{data['projected_percent']:.2f}%</span>", unsafe_allow_html=True)
                if not data["is_safe"]:
                    st.warning(f"CRITICAL RISK: You must attend {data['recovery_classes_needed']} consecutive classes to recover.")
            
            if student_name and event_name:
                pdf_filename = generate_duty_leave_pdf(student_name, event_name, actual_missed, results)
                
                with open(pdf_filename, "rb") as pdf_file:
                    pdf_bytes = pdf_file.read()
                    
                st.download_button(
                    label="📥 Download Official Duty Leave PDF",
                    data=pdf_bytes,
                    file_name=pdf_filename,
                    mime="application/pdf"
                )
            else:
                st.info("Enter your Student Name and Event Name to unlock the PDF download.")
                
            st.session_state.analyzer.planned_leaves = []