import streamlit as st
import pandas as pd
from datetime import datetime

# --- APP INTERFACE ---
st.set_page_config(page_title="Limitless OEE Portal", layout="centered")

st.markdown("<h1 style='text-align: center; color: #1E88E5;'>⚙️ LIMITLESS OEE PORTAL</h1>", unsafe_allow_html=True)
st.write("---")

# Input Fields
asset = st.selectbox("🏭 Select Asset", ["PUMP-01", "CONVEYOR-01", "BLENDER-02", "FILLER-04"])
event = st.selectbox("🚦 Event Type", ["FAILURE", "IDLE", "PM"])
reason = st.text_input("🔍 Root Cause / Reason", "N/A")
start_time = st.text_input("🕒 Start (YYYY-MM-DD HH:MM)", datetime.now().strftime('%Y-%m-%d %H:00'))
end_time = st.text_input("🏁 End (YYYY-MM-DD HH:MM)")

if st.button("🚀 SUBMIT TO DRIVE"):
    if not end_time:
        st.warning("Please enter an end time.")
    else:
        st.success(f"✅ Data for {asset} ready to sync!")
        st.balloons()
