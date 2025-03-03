import streamlit as st
from streamlit_webrtc import webrtc_streamer

st.title("Minimal WebRTC Test")
webrtc_streamer(
    key="test",
    media_stream_constraints={
        "video": {
            "width": {"ideal": 320},
            "height": {"ideal": 240},
            "frameRate": {"ideal": 10}
        },
        "audio": False
    }
)

