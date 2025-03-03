import cv2
import streamlit as st
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer
from handtracking_module import HandDetector  # Make sure class names match

class HandTrackingTransformer(VideoTransformerBase):
    def __init__(self):
        self.detector = HandDetector(maxHands=1)
    
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img = self.detector.findHands(img, draw=True)
        lmList, bbox = self.detector.findPosition(img, draw=True)
        if lmList:
            cv2.putText(img, "Hand Detected", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        return img

st.title("Real-Time Hand Tracking")
st.markdown("This app demonstrates real-time hand tracking using MediaPipe and OpenCV.")

webrtc_streamer(
    key="hand-tracker",
    video_transformer_factory=HandTrackingTransformer,
    media_stream_constraints={
        "video": {
            "width": {"ideal": 640},
            "height": {"ideal": 480},
            "frameRate": {"ideal": 15}
        },
        "audio": False
    }
)
