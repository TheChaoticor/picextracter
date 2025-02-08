import streamlit as st
import cv2
import numpy as np
import os
import zipfile
from io import BytesIO
from PIL import Image

def extract_frames(video_path, interval=30):
    cap = cv2.VideoCapture(video_path)
    frame_list = []
    count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if count % interval == 0:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_list.append(frame)
        count += 1
    
    cap.release()
    return frame_list

def save_frame_as_image(frame):
    img = Image.fromarray(frame)
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def create_zip(frames):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        for i, frame in enumerate(frames):
            img_data = save_frame_as_image(frame)
            zf.writestr(f"frame_{i}.png", img_data)
    zip_buffer.seek(0)
    return zip_buffer

st.title("Video Frame Extractor")

uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov", "mkv"])

if uploaded_file:
    temp_video_path = "temp_video.mp4"
    with open(temp_video_path, "wb") as f:
        f.write(uploaded_file.read())
    
    interval = st.slider("Select frame interval", min_value=1, max_value=100, value=30)
    frames = extract_frames(temp_video_path, interval)
    
    st.write(f"Extracted {len(frames)} frames")
    
    for i, frame in enumerate(frames):
        st.image(frame, caption=f"Frame {i * interval}", use_column_width=True)
        btn = st.download_button(
            label="Download Frame",
            data=save_frame_as_image(frame),
            file_name=f"frame_{i}.png",
            mime="image/png"
        )
    
    if frames:
        zip_file = create_zip(frames)
        st.download_button(
            label="Download All Frames as ZIP",
            data=zip_file,
            file_name="frames.zip",
            mime="application/zip"
        )
