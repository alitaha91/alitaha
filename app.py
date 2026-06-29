import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, time

# 1. Connection Logic (Uses your existing Secrets)
def get_sheet():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
    client = gspread.authorize(creds)
    return client.open("Limitless_OEE_Database").sheet1

# 2. Page Configuration
st.set_page_config(page_title="Limitless Reliability Portal", page_icon="⚙️", layout="centered")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #004a99; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏭 Limitless Reliability Tracking Log")
st.info("Engineering Maintenance Department")

# 3. Machine & Station Configurations
machines = [
    "SuperPack Sachet Filling", "Bosch Capsule filling", "Bohle Bin Blender", 
    "VG Fielder", "Oven Tray Dryer", 
    "Glatt Coater", "Great Pack Sachet Filling", 
    "Fette Compression Machine 1", "Marchesini Blistering Machine", "Countec Line", 
    "Klockner blistering Machine", 
    "Fette Compression Machine 2", "Glatt Fluid Bed"
]

station_mapping = {
    "Klockner blistering Machine": ["Reel Winder", "Forming", "Feeding", "Sealing", "Punching", "Waste Shredder", "Discharge"],
    "Marchesini Blistering Machine": ["Reel Winder", "Forming", "Feeding", "Sealing", "Punching", "Waste Shredder", "Discharge"],
    "SuperPack Sachet Filling": ["Feeding Hopper", "Filling", "Vertical Sealing", "Horizontal Sealing", "Printing", "Cutting", "Discharge"],
    "Great Pack Sachet Filling": ["Feeding Hopper", "Filling", "Vertical Sealing", "Horizontal Sealing", "Printing", "Cutting", "Discharge"]
}

# 4. Interactive Selectors (Outside form context to ensure reactive state changes)
col1, col2 = st.columns(2)
with col1:
    asset = st.selectbox("Select Machine", sorted(machines))
with col2:
    event = st.selectbox("Event Type", ["FAILURE", "IDLE", "In-Operation", "SETUP"])

# Manage conditional visibility next to details
selected_station = "N/A"
if event == "FAILURE":
    c_det1, c_det2 = st.columns(2)
    with c_det1:
        reason = st.text_input("Failure Details")
    with c_det2:
        if asset in station_mapping:
            selected_station = st.selectbox("Select Failed Station", station_mapping[asset])
        else:
            selected_station = st.text_input("Specify Station / Assembly", value="General")
else:
    # If not a failure, hide the station dropdown entirely and just show details
    reason = st.text_input("Log Details")

# 5. Core Form for Datetime & Submit Process
with st.form("oee_time_form", clear_on_submit=True):
    st.subheader("🕒 Downtime Period")
    c3, c4 = st.columns(2)
    with c3:
        d_start = st.date_input("Start Date", datetime.now())
        t_start = st.time_input("Start Time", time(8, 0), step=60)
    with c4:
        d_end = st.date_input("End Date", datetime.now())
        t_end = st.time_input("End Time", time(16, 0), step=60)

    submit = st.form_submit_button("🚀 SYNC TO MAINTENANCE LOG")

# 6. Submission Execution
if submit:
    if not reason:
        st.error("Missing Data: Please enter a details/root cause description.")
    else:
        try:
            start_dt = datetime.combine(d_start, t_start).strftime("%Y-%m-%d %H:%M")
            end_dt = datetime.combine(d_end, t_end).strftime("%Y-%m-%d %H:%M")
            
            sheet = get_sheet()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Formats logged row clearly in Google Sheets
            sheet.append_row([timestamp, asset, event, reason, start_dt, end_dt, selected_station])
            
            st.success(f"✅ Data for {asset} successfully logged!")
            st.balloons()
        except Exception as e:
            st.error(f"Sync failed. Check API connection details: {e}")
