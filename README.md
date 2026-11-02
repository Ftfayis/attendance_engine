# OptiLeave: Academic Compliance & Risk Engine

An automated, AI-powered Streamlit web application designed to calculate attendance risk, forecast post-leave academic standing, and generate formal Duty Leave (DL) documentation. 

This engine shifts away from traditional "class-based" counting to precise "hour-based" metrics, aligning with standard university compliance regulations.

## 🚀 Key Features

* **AI Timetable Ingestion:** Seamlessly extracts subjects and scheduled weekly hours directly from a screenshot of a timetable using the Google Gemini 3.8 Flash vision model.
* **Hour-Based Risk Simulation:** Calculates current attendance percentages and mathematically projects future standing based on proposed absence hours.
* **Automated PDF Generation:** Instantly compiles a formal, print-ready Duty Leave (DL) application complete with risk assessment data for Head of Department (HOD) approval.
* **Interactive Dashboard:** Built with Streamlit for a responsive, real-time user experience featuring session state memory for quick subject toggling.

## 🛠️ Technology Stack

* **Frontend & State Management:** Python, Streamlit
* **AI & Computer Vision:** Google GenAI SDK (`gemini-3.8-flash`)
* **Document Generation:** FPDF
* **Version Control:** Git, GitHub

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/attendance_engine.git](https://github.com/yourusername/attendance_engine.git)
   cd attendance_engine