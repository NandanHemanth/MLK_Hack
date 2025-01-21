import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import datetime
import time as tm
import base64

# Convert local image to Base64
def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Base64 encoded logo (replace "logo.png" with your logo file path)
logo_base64 = get_image_base64("logo.png")

# Add CSS for styling, logo, and modal popups
st.markdown(
    f"""
    <style>
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    body {{
        background-color: #800020; /* Burgundy Red */
        color: white; /* Make text white for better contrast */
        font-family: 'IBM Plex Sans', sans-serif; /* Set font globally */
    }}
    .stApp {{
        background-color: #800020 !important; /* Ensure main content has the same background */
        color: white; /* Set default text color */
        font-family: 'IBM Plex Sans', sans-serif;
    }}
    div[data-testid="stSidebar"] {{
        background-color: #800020 !important; /* Sidebar background */
        color: white;
        font-family: 'IBM Plex Sans', sans-serif;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: white !important; /* Ensure headings remain visible */
        font-family: 'IBM Plex Sans', sans-serif;
    }}
    .logo-container {{
        position: fixed;
        top: 10px;
        right: 10px;
        z-index: 10;
    }}
    .logo {{
        width: 120px; /* Adjust the size of the logo */
    }}
    .center-buttons {{
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-top: 20px;
    }}
    .button {{
        width: 200px;
        padding: 10px 0;
        font-size: 18px;
        text-align: center;
        background-color: white;
        color: #800020;
        border: none;
        border-radius: 8px;
        font-family: 'IBM Plex Sans', sans-serif;
        cursor: pointer;
    }}
    .modal-container {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(5px);
        z-index: 1000;
        display: flex;
        justify-content: center;
        align-items: center;
    }}
    .modal-content {{
        background-color: white;
        color: #800020;
        padding: 20px;
        border-radius: 10px;
        width: 50%;
        text-align: center;
        font-family: 'IBM Plex Sans', sans-serif;
    }}
    .close-button {{
        background: none;
        border: none;
        font-size: 20px;
        font-weight: bold;
        color: red;
        cursor: pointer;
        position: absolute;
        top: 10px;
        right: 20px;
    }}
    </style>
    <div class="logo-container">
        <img src="data:image/png;base64,{logo_base64}" alt="Logo" class="logo">
    </div>
    """,
    unsafe_allow_html=True
)

# Hackathon Itinerary Data
itinerary = [
    ("3:30 PM", "Reporting Time"),
    ("3:45 - 4:30 PM", "Check-in Begins"),
    ("4:30 - 5:00 PM", "Opening Ceremony"),
    ("5:00 PM", "Hackathon Begins"),
    ("8:00 - 9:00 PM", "Dinner"),
    ("12:00 - 1:00 AM", "Games and Refreshments"),
    ("7:00 - 7:30 AM", "Morning Energizer"),
    ("9:00 - 10:00 AM", "Breakfast"),
    ("1:30 - 2:30 PM", "Late Lunch"),
    ("5:00 PM", "Hackathon Ends"),
    ("5:00 - 6:00 PM", "Judging"),
    ("6:00 - 6:30 PM", "Break"),
    ("6:30 - 7:00 PM", "Prize Distribution and Closing")
]

# Heading and Description
st.title("MLK Hackathon")
st.write("Welcome to the MLK Hackathon! ")

# Create Directed Graph for Timeline
G = nx.DiGraph()
for i, (time, event) in enumerate(itinerary):
    G.add_node(i, time=time, event=event)
    if i > 0:
        G.add_edge(i - 1, i)

# Sidebar with Timeline Graph
with st.sidebar:
    st.header("Hackathon Timeline")
    plt.figure(figsize=(4, 20))  # Increase figure height for longer edges
    pos = {i: (0, -i * 1.5) for i in range(len(itinerary))}  # Increase vertical spacing between nodes
    nx.draw(G, pos, with_labels=False, node_size=3000, node_color='skyblue', edge_color='gray')
    labels = {i: f"{data['time']}\n{data['event']}" for i, data in G.nodes(data=True)}
    nx.draw_networkx_labels(G, pos, labels, font_size=10, font_weight='bold', verticalalignment='center')
    plt.title("Timeline")
    st.pyplot(plt)

    st.markdown("---")
    st.header("Hackathon Overview")
    st.write("**Hackathon Duration:**\n\n  🕒 *January 30th, 5:00 PM - January 31st, 5:00 PM* ")
    st.write("**Prize Distribution:**\n\n 🏆 *January 31st, 6:30 PM - 7:00 PM* ")
    st.write("Good luck to all participants! Let's make this a memorable event.")

# Main Page and Timer:
# Timer Configuration
start_date = datetime.datetime(2025, 1, 30, 17, 0, 0)  # Jan 30, 5:00 PM
end_date = start_date + datetime.timedelta(hours=24)  # 24-hour timer

# Timer Display
current_time = datetime.datetime.now()
time_left = end_date - current_time

if current_time < start_date:
    countdown = start_date - current_time
    days, seconds = divmod(countdown.total_seconds(), 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    st.markdown(f"<h1 style='text-align: center; font-size: 50px;'>⏳ Hackathon starts in:</h1>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center; font-size: 150px;'>{int(days):02d}:{int(hours):02d}:{int(minutes):02d}</h1>", unsafe_allow_html=True)
elif time_left.total_seconds() > 0:
    days, seconds = divmod(time_left.total_seconds(), 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    st.markdown(f"<h1 style='text-align: center; font-size: 50px;'>⏳ Time Remaining:</h1>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center; font-size: 150px;'>{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center; font-size: 50px;'>🎉 The Hackathon has ended!</h1>", unsafe_allow_html=True)

# Announcements Section
st.markdown("---")
st.header("📢 Announcements")
announcements = [
    "1. Judging starts at 5:00 PM.",
    "2. Refreshments are available in the main hall.",
    "3. Submit your final projects by 4:30 PM."
]
for announcement in announcements:
    st.write(announcement)

st.markdown("")
st.markdown("")

# Manage modal visibility
if "show_tracks_modal" not in st.session_state:
    st.session_state["show_tracks_modal"] = False

if "show_help_modal" not in st.session_state:
    st.session_state["show_help_modal"] = False

# Centered Buttons Section
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("View Tracks"):
        st.session_state["show_tracks_modal"] = True
        st.session_state["show_help_modal"] = False  # Close help modal if open

with col2:
    if st.button("Help"):
        st.session_state["show_help_modal"] = True
        st.session_state["show_tracks_modal"] = False  # Close tracks modal if open

# Render Tracks Modal
if st.session_state["show_tracks_modal"]:
    st.markdown(
        """
        <div class="modal-container">
            <div class="modal-content">
                <button class="close-button" onclick="window.location.reload();">×</button>
                <h2>Hackathon Tracks</h2>
                <p>1. Education System Improvement</p>
                <p>2. Healthcare Innovation</p>
                <p>3. Social Impact for People with Disabilities</p>
                <p>4. Creative Wildcard</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Render Help Modal
if st.session_state["show_help_modal"]:
    st.markdown(
        """
        <div class="modal-container">
            <div class="modal-content">
                <button class="close-button" onclick="window.location.reload();">×</button>
                <h2>Help & Support</h2>
                <p>Need assistance? Contact us:</p>
                <p>Email: support@mlkhackathon.com</p>
                <p>Phone: +1-800-123-4567</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Auto-refresh Timer (use Streamlit Auto Refresh workaround)
tm.sleep(1)
st.rerun()
