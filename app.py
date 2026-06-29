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
st.set_page_config(page_title="Limitless OEE Portal", page_icon="⚙️", layout="centered")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #004a99; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏭 Limitless OEE Log")
st.info("Electrical & Maintenance Department Portal")

# 3. Your Real Machine List & Dynamic Stations Mapping
machines = [
    "SuperPack Sachet Filling", "Bosch Capsule filling", "Bohle Bin Blender", 
    "Quadro Mill 1", "Quadro Mill 2", "VG Fielder", "Oven Tray Dryer", 
    "Glatt Coater", "Gea Coater Lifter", "Killian Compression Machine", 
    "Automatic Labelling Machine", "All Fill Powder Filling", "Great Pack Sachet Filling", 
    "Fette Compression Machine 1", "Compact Russell Sieve", "ServoLift Lifter", 
    "Frewitt Mill", "Marchesini Blistering Machine", "Tablet Counting Machine", 
    "Autmatic Induction Sealing", "Capping Machine", "Klockner blistering Machine", 
    "Garvens CheckWeigher 1", "Garvens CheckWeigher 2", "Oscillating Frewitt Mill", 
    "Russel Sieve", "Fette Compression Machine 2", "Glatt Fluid Bed"
]

# Mapping machines to their respective functional stations
station_mapping = {
    "Klockner blistering Machine": ["Reel Winder", "Forming", "Feeding", "Sealing", "Punching", "Waste Shredder", "Discharge"],
    "Marchesini Blistering Machine": ["Reel Winder", "Forming", "Feeding", "Sealing", "Punching", "Waste Shredder", "Discharge"],
    "SuperPack Sachet Filling": ["Feeding Hopper", "Filling", "Vertical Sealing", "Horizontal Sealing", "Printing", "Cutting", "Discharge"],
    "Great Pack Sachet Filling": ["Feeding Hopper", "Filling", "Vertical Sealing", "Horizontal Sealing", "Printing", "Cutting", "Discharge"]  # Mapped for consistency
}

# 4. Input Form with Calendar View
with st.form("oee_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        asset = st.selectbox("Select Machine", sorted(machines))
        event = st.selectbox("Event Type", ["FAILURE", "IDLE", "PM", "SETUP"])
    with col2:
        reason = st.text_input("Root Cause / Breakdown Detail")
        
    # Dynamic Station logic: Appears only when Event Type is FAILURE
    selected_station = "N/A"  # Default if not a failure or not a mapped machine
    if event == "FAILURE":
        st.write("---")
        st.subheader("🛠️ Failure Location Tracking")
        
        # Check if the selected machine has specific stations defined
        if asset in station_mapping:
            selected_station = st.selectbox("Select Failed Station / Module", station_mapping[asset])
        else:
            # Fallback for other machines on your list
            selected_station = st.text_input("Specify Station / Assembly (Optional)", value="General Mechanical")

    st.write("---")
    st.subheader("🕒 Downtime Period")
    
    c3, c4 = st.columns(2)
    with c3:
        d_start = st.date_input("Start Date", datetime.now())
        t_start = st.time_input("Start Time", time(8, 0), step=60)
    with c4:
        d_end = st.date_input("End Date", datetime.now())
        t_end = st.time_input("End Time", time(16, 0), step=60)

    submit = st.form_submit_button("🚀 SYNC TO MAINTENANCE LOG")

# 5. Submission Execution
if submit:
    if not reason:
        st.error("Missing Data: Please enter a reason/root cause.")
    else:
        try:
            start_dt = datetime.combine(d_start, t_start).strftime("%Y-%m-%d %H:%M")
            end_dt = datetime.combine(d_end, t_end).strftime("%Y-%m-%d %H:%M")
            
            sheet = get_sheet()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Appending rows: Timestamp, Machine, Event, Reason, Start, End, Station Location
            sheet.append_row([timestamp, asset, event, reason, start_dt, end_dt, selected_station])
            
            st.success(f"✅ Data for {asset} ({selected_station}) successfully synced to Google Sheets!")
            st.balloons()
        except Exception as e:
            st.error(f"Sync failed. Check if Google Drive/Sheets API is enabled: {e}")
