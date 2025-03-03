import cv2
import streamlit as st
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer
from handtracking_module import HandDetector

# Example transformer class
class HandTrackingTransformer(VideoTransformerBase):
    def __init__(self):
        self.detector = HandDetector(maxHands=1)
    
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        # Process the frame (detect hands, draw landmarks, etc.)
        img = self.detector.findHands(img)
        return img

st.title("Real-Time Hand Tracking")
st.markdown("This app demonstrates real-time hand tracking using MediaPipe and OpenCV.")

webrtc_streamer(
    key="hand-tracker",
    video_transformer_factory=HandTrackingTransformer,
    # ↓ ADD THESE PARAMETERS ↓
    media_stream_constraints={
        "video": {
            "width": {"ideal": 640},     # reduce resolution to save memory
            "height": {"ideal": 480},
            "frameRate": {"ideal": 15}   # lower FPS to reduce CPU usage
        },
        "audio": False
    },
    max_clients=1  # limit concurrent users to reduce resource usage
)
