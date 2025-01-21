import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import datetime
import time as tm

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
st.title("MLK Hackathon Itinerary")
st.write("Welcome to the MLK Hackathon! Here's a breakdown of the schedule:")

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

# Auto-refresh Timer (use Streamlit Auto Refresh workaround)
tm.sleep(1)
st.rerun()

