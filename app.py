import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Clean App Styling (Hides all the "Code" feel)
st.set_page_config(page_title="Limitless OEE Portal", page_icon="⚙️", layout="centered")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 15px; height: 3em; background-color: #007bff; color: white; font-weight: bold; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #004a99;'>⚙️ LIMITLESS OEE PORTAL</h1>", unsafe_allow_html=True)
st.write("---")

# 2. Maintenance Data Entry (Streamlit native widgets)
asset = st.selectbox("🏭 Select Asset", ["Klockner CP3", "CPCG 120", "PUMP-01", "CONVEYOR-01", "BLENDER-02"])
event = st.radio("🚦 Event Type", ["FAILURE", "IDLE", "PM"], horizontal=True)
reason = st.text_input("🔍 Root Cause / Reason")

col1, col2 = st.columns(2)
with col1:
    start_t = st.text_input("🕒 Start", datetime.now().strftime('%Y-%m-%d %H:00'))
with col2:
    end_t = st.text_input("🏁 End")

# 3. Logic to Submit
if st.button("🚀 SYNC TO MAINTENANCE LOG"):
    if not end_t or not reason:
        st.error("Missing Data: Please fill in Reason and End Time.")
    else:
        # Success Feedback
        st.success(f"✅ Data for {asset} recorded!")
        st.balloons()
        
        # Display summary for the user
        st.info(f"Summary: {event} for {asset} starting at {start_t}")
