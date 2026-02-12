# student_main.py
import streamlit as st
from ATTENDANCE.student import show_student_panel
import pandas as pd
from ATTENDANCE.clients import create_supabase_client
from datetime import datetime
from ATTENDANCE.attendance_panel import show_attendance_panel
import pytz

st.set_page_config(
    page_title="Student Portal",
    layout="centered",
    page_icon="🎓"
)

# Supabase Client for view-attendance tab
try:
    supabase = create_supabase_client()
except Exception:
    supabase = None

def current_ist_date():
    return datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d")

st.markdown("""
<h1 style='text-align: center; color: #4B8BBE;'>🎓 Student Attendance Portal</h1>
<hr style='border-top: 1px solid #bbb;' />
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📥 Mark Attendance", "📅 View My Attendance"])

with tab1:
    show_student_panel()

with tab2:
    show_attendance_panel()