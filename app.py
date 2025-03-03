# app.py
import cv2
import streamlit as st
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer
from HandTrackingModule import HandDetector


# Define a transformer that will process video frames
class HandTrackingTransformer(VideoTransformerBase):
    def __init__(self):
        self.detector = HandDetector(maxHands=1)
    
    def transform(self, frame):
        # Convert the incoming frame to a NumPy array (BGR format)
        img = frame.to_ndarray(format="bgr24")
        # Process the image to detect and draw hand landmarks
        img = self.detector.findHands(img, draw=True)
        lmList, bbox = self.detector.findPosition(img, draw=True)
        # (Optional) Show a message if a hand is detected
        if lmList:
            cv2.putText(img, "Hand Detected", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        return img

# Streamlit app UI
st.title("Real‑Time Hand Tracking")
st.markdown("This app demonstrates real‑time hand tracking using MediaPipe and OpenCV.")

# Start the webcam stream with the defined transformer
webrtc_streamer(key="hand-tracker", video_transformer_factory=HandTrackingTransformer)
