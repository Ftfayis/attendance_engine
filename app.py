# app.py
import streamlit as st
from models import Subject, LeaveEvent, RiskAnalyzer

if "analyzer" not in st.session_state:
    st.session_state.analyzer = RiskAnalyzer()

st.title("Attendance Risk & Forecasting Engine")

st.header("1. Add Subject Data")
with st.form("add_subject_form"):
    sub_name = st.text_input("Subject Name (e.g., Microcontrollers)")
    total_held = st.number_input("Total Classes Held", min_value=0, step=1)
    attended = st.number_input("Classes Attended", min_value=0, step=1)
    submit_subject = st.form_submit_button("Add Subject")

    if submit_subject and sub_name:
        new_sub = Subject(sub_name, total_held, attended)
        st.session_state.analyzer.add_subject(new_sub)
        st.success(f"Added {sub_name}!")

st.header("2. Current Academic Standing")
if st.session_state.analyzer.subjects:
    for name, sub in st.session_state.analyzer.subjects.items():
        st.metric(
            label=name, 
            value=f"{sub.get_current_percentage():.2f}%", 
            delta=f"{sub.get_remaining_safe_cuts()} safe cuts left"
        )
else:
    st.info("No subjects added yet.")

st.header("3. Simulate Future Leave")
with st.form("simulate_leave_form"):
    event_name = st.text_input("Event Name (e.g., IGNITE 2.0 Ideathon)")
    
    st.write("Specify missed classes per subject:")
    missed_counts = {}
    for sub_name in st.session_state.analyzer.subjects.keys():
        missed_counts[sub_name] = st.number_input(f"Missed {sub_name} classes", min_value=0, step=1)
        
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
        
        st.session_state.analyzer.planned_leaves = []