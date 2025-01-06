import streamlit as st
import datetime
import time

# Main Page Title
st.title("MLK Hackathon")

# Timer Configuration
start_date = datetime.datetime(2025, 1, 5, 20, 4, 0)  # Jan 30, 5:00 PM
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
    st.markdown(f"<h1 style='text-align: center; font-size: 150px;'>{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}</h1>", unsafe_allow_html=True)
elif time_left.total_seconds() > 0:
    days, seconds = divmod(time_left.total_seconds(), 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    st.markdown(f"<h1 style='text-align: center; font-size: 50px;'>⏳ Time Remaining:</h1>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center; font-size: 150px;'>{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center; font-size: 50px;'>🎉 The Hackathon has ended!</h1>", unsafe_allow_html=True)

# Auto-refresh Timer (use Streamlit Auto Refresh workaround)
time.sleep(1)
st.rerun()