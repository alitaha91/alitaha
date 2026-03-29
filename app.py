import streamlit as st
from datetime import datetime

# 1. Page Configuration (This makes it look like a clean app)
st.set_page_config(page_title="Limitless OEE Portal", page_icon="⚙️", layout="centered")

# 2. Creative Styling
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #007bff; color: white; font-weight: bold; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #004a99;'>⚙️ LIMITLESS OEE PORTAL</h1>", unsafe_allow_html=True)
st.write("---")

# 3. Data Entry Form
with st.container():
    asset = st.selectbox("🏭 Select Asset", ["PUMP-01", "CONVEYOR-01", "BLENDER-02", "FILLER-04", "Klockner CP3", "CPCG 120"])
    event = st.radio("🚦 Event Type", ["FAILURE", "IDLE", "PM"], horizontal=True)
    reason = st.text_input("🔍 Root Cause / Reason")
    
    col1, col2 = st.columns(2)
    with col1:
        start_time = st.text_input("🕒 Start", datetime.now().strftime('%Y-%m-%d %H:00'))
    with col2:
        end_time = st.text_input("🏁 End")

# 4. Submission Logic
if st.button("🚀 SYNC TO MAINTENANCE LOG"):
    if not end_time or not reason:
        st.error("Please fill in all fields before submitting.")
    else:
        st.success(f"✅ Logged {asset} successfully!")
        st.balloons()

# --- 4. DISPLAY THE APP ---
app = widgets.VBox([header_box, asset, event, reason, start_t, end_t, btn, output],
                   layout=widgets.Layout(align_items='center', padding='20px', background_color='#fdfefe', border='1px solid #ddd', border_radius='15px'))
display(app)
