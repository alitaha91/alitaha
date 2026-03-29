# @title Default title text
from google.colab import auth
from google.auth import default

# --- 1. AUTHENTICATION & AUTO-CREATE LOGIC ---
auth.authenticate_user()
creds, _ = default()
gc = gspread.authorize(creds)

FILE_NAME = "Limitless_OEE_Database" # This will be the name of the file in your Drive

def get_or_create_sheet():
    try:
        # Try to open the file
        spreadsheet = gc.open(FILE_NAME)
    except gspread.exceptions.SpreadsheetNotFound:
        # If not found, create it!
        print(f"✨ Creating new file: {FILE_NAME} in your Google Drive...")
        spreadsheet = gc.create(FILE_NAME)
        # Share it with yourself (standard for Colab)
        # Note: It's already in your drive, but this ensures accessibility.

    try:
        # Try to find the OEE tab
        worksheet = spreadsheet.worksheet("OEE")
    except gspread.exceptions.WorksheetNotFound:
        # Create OEE tab if it's missing
        worksheet = spreadsheet.add_worksheet(title="OEE", rows="1000", cols="10")
        # Add Headers for CMRP/OEE tracking
        headers = ["Machine ID", "Event Type", "Reason/Code", "Start Time", "End Time", "Duration (Hrs)", "Log Date"]
        worksheet.append_row(headers)

    return worksheet

# Initialize the sheet
sh = get_or_create_sheet()

# --- 2. CREATIVE UI COMPONENTS ---
header_box = widgets.HTML("""
<div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
    <h1 style="color: white; margin: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">⚙️ LIMITLESS OEE PORTAL</h1>
    <p style="color: #d1d1d1; font-size: 14px;">Real-Time Maintenance & Reliability Synchronization</p>
</div>
""")

# Input Fields
style = {'description_width': '120px'}
layout = widgets.Layout(width='400px', margin='10px 0')

asset = widgets.Dropdown(options=["PUMP-01", "CONVEYOR-01", "BLENDER-02", "FILLER-04"], description='🏭 Asset ID:', style=style, layout=layout)
event = widgets.Dropdown(options=[("Breakdown (Failure)", "FAILURE"), ("Idle (No Plan)", "IDLE"), ("Planned PM", "PM")], description='🚦 Event Type:', style=style, layout=layout)
reason = widgets.Dropdown(options=["Mechanical", "Electrical", "Operational", "Lubrication", "Cleaning", "N/A"], description='🔍 Root Cause:', style=style, layout=layout)
start_t = widgets.Text(value=datetime.now().strftime('%Y-%m-%d %H:00'), description='🕒 Start:', style=style, layout=layout)
end_t = widgets.Text(placeholder='YYYY-MM-DD HH:MM', description='🏁 End:', style=style, layout=layout)

# Action Button
btn = widgets.Button(description='SYNC TO DRIVE', button_style='primary', icon='cloud-upload', layout=widgets.Layout(width='400px', height='50px', margin='20px 0'))
output = widgets.Output()

# --- 3. SUBMISSION LOGIC ---
def handle_submit(b):
    with output:
        clear_output()
        try:
            # Calculate Duration
            s = datetime.strptime(start_t.value, '%Y-%m-%d %H:%M')
            e = datetime.strptime(end_t.value, '%Y-%m-%d %H:%M')
            duration = round((e - s).total_seconds() / 3600, 2)

            if duration <= 0:
                print("⚠️ Error: End time must be after Start time.")
                return

            # Append Data
            row = [asset.value, event.value, reason.value, start_t.value, end_t.value, duration, datetime.now().strftime('%Y-%m-%d %H:%M')]
            sh.append_row(row)

            # Creative Success Message
            display(widgets.HTML(f"<div style='color: #27ae60; font-weight: bold; border: 1px solid #27ae60; padding: 10px; border-radius: 5px;'>✅ SUCCESS: {asset.value} logged for {duration} hours!</div>"))

            # Reset End Time
            end_t.value = ""

        except Exception as err:
            display(widgets.HTML(f"<div style='color: #c0392b; font-weight: bold;'>❌ FORMAT ERROR: Use YYYY-MM-DD HH:MM</div>"))

btn.on_click(handle_submit)

# --- 4. DISPLAY THE APP ---
app = widgets.VBox([header_box, asset, event, reason, start_t, end_t, btn, output],
                   layout=widgets.Layout(align_items='center', padding='20px', background_color='#fdfefe', border='1px solid #ddd', border_radius='15px'))
display(app)
