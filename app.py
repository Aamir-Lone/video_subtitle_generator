# app.py
import streamlit as st
import tempfile
import os
# from moviepy import VideoFileClip, AudioFileClip
from moviepy.editor import VideoFileClip
import whisper
import srt
from datetime import timedelta

# Import your render function from dynamic-subs
from dynamic_subs import render_subtitles  

st.title("Video Subtitle Generator")

# Upload video
uploaded_file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi", "mkv"])

# Subtitle options
st.sidebar.header("Subtitle Settings")
font_size = st.sidebar.slider("Font Size", 20, 80, 40)
font_color = st.sidebar.color_picker("Font Color", "#ffffff")
bg_color = st.sidebar.color_picker("Background Color", "#000000")
output_format = st.sidebar.selectbox("Output Subtitle Format", ["Hardcoded (Video)", "SRT File"])

if uploaded_file:
    st.video(uploaded_file)

    if st.button("Generate Subtitles"):
        with st.spinner("Processing video..."):
            # Save uploaded video to temp file
            temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
            temp_video.write(uploaded_file.read())
            temp_video.close()

            # Transcribe with Whisper
            model = whisper.load_model("base")
            result = model.transcribe(temp_video.name)

            # Build transcript list
            transcript = []
            for seg in result['segments']:
                transcript.append({
                    "start": seg['start'],
                    "end": seg['end'],
                    "text": seg['text']
                })

            # Output video + subtitle paths
            output_video_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
            output_srt_path = tempfile.NamedTemporaryFile(delete=False, suffix=".srt").name

            if output_format == "Hardcoded (Video)":
                render_subtitles(
                    temp_video.name,
                    output_video_path,
                    transcript,
                    dynamic_colors=True,
                    
                )
                st.success("Subtitled video generated ✅")
                st.video(output_video_path)

                with open(output_video_path, "rb") as f:
                    st.download_button("Download Video", f, file_name="subtitled_video.mp4")

            else:
                # Generate SRT file
                subs = []
                for i, seg in enumerate(transcript, start=1):
                    subs.append(srt.Subtitle(
                        index=i,
                        start=timedelta(seconds=seg["start"]),
                        end=timedelta(seconds=seg["end"]),
                        content=seg["text"].strip()
                    ))
                with open(output_srt_path, "w", encoding="utf-8") as f:
                    f.write(srt.compose(subs))

                st.success("Subtitle file generated ✅")
                with open(output_srt_path, "rb") as f:
                    st.download_button("Download SRT", f, file_name="subtitles.srt")
