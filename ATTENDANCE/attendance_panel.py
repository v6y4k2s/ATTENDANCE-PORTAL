import streamlit as st
import supabase
import pandas as pd
from .logger import get_log
from .clients import create_supabase_client

logger=get_log(__name__)

try:
    supabase = create_supabase_client()
except Exception:
    supabase = None

def show_attendance_panel():
    st.subheader("📅 Check Your Attendance Record")

    with st.form("view_attendance_form"):
        if supabase:
            try:
                class_rows = supabase.table("classroom_settings").select("class_name").execute().data or []
                class_list = [entry["class_name"] for entry in class_rows]
            except Exception:
                class_list = []
        else:
            class_list = []

        selected_class = st.selectbox("Select Your Class", class_list)
        roll_number = st.text_input("Enter Your Roll Number").strip()
        submit = st.form_submit_button("🔍 Show My Attendance")

    if submit:
        if not roll_number:
            st.warning("Please enter your roll number.")
        else:
            if not supabase:
                st.error("Supabase client is not initialized.")
            else:
                try:
                    records = (
                        supabase.table("attendance")
                        .select("*")
                        .eq("class_name", selected_class)
                        .eq("roll_number", roll_number)
                        .execute()
                        .data
                    )
                except Exception:
                    records = []

                if not records:
                    st.info("No attendance found for this roll number.")
                else:
                    df = pd.DataFrame(records)
                    df["status"] = "P"

                    matrix = df.pivot_table(
                        index=["roll_number", "name"],
                        columns="date",
                        values="status",
                        aggfunc="first",
                        fill_value="A"
                    ).reset_index()

                    matrix.columns.name = None
                    matrix = matrix.sort_values("roll_number")

                    st.dataframe(matrix, use_container_width="True")
