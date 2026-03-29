import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Connection logic
def get_sheet():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
    client = gspread.authorize(creds)
    # CHANGE THIS to your exact Google Sheet name
    return client.open("Limitless_OEE_Database").sheet1

st.set_page_config(page_title="Limitless OEE Portal", layout="centered")
st.markdown("<h1 style='text-align: center;'>⚙️ LIMITLESS OEE PORTAL</h1>", unsafe_allow_html=True)

asset = st.selectbox("🏭 Select Asset", ["Klockner CP3", "CPCG 120", "PUMP-01"])
event = st.radio("🚦 Event Type", ["FAILURE", "IDLE", "PM"], horizontal=True)
reason = st.text_input("🔍 Root Cause / Reason")
start_t = st.text_input("🕒 Start", datetime.now().strftime('%Y-%m-%d %H:00'))
end_t = st.text_input("🏁 End")

if st.button("🚀 SYNC TO MAINTENANCE LOG"):
    if not end_t or not reason:
        st.error("Please provide a reason and end time.")
    else:
        try:
            sheet = get_sheet()
            sheet.append_row([str(datetime.now()), asset, event, reason, start_t, end_t])
            st.success(f"✅ Data for {asset} synced to Google Sheets!")
            st.balloons()
        except Exception as e:
            st.error(f"Sync failed: {e}")
