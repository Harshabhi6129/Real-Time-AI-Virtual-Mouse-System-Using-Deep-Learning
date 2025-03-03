import streamlit as st
from streamlit_webrtc import webrtc_streamer

st.title("Minimal WebRTC Test")
webrtc_streamer(key="test")
