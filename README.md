# 🎥 Video Subtitle Generator

A **Video Subtitle Generator** web app that extracts audio from uploaded videos, generates transcripts, and overlays subtitles on the video.  
This project is built using **Streamlit**, **OpenAI Whisper**, and **MoviePy**, providing both **soft subtitle (.srt)** and **hardcoded subtitle video** outputs.  

🚀 **Live Demo:** [subtitlegeneratorfromvideo.streamlit.app](https://subtitlegeneratorfromvideo.streamlit.app/)

---

## ✨ Features

- 📤 Upload any video file.
- 🎙️ Extract audio and transcribe using **Whisper**.
- 📝 Generate subtitles in `.srt` format.
- 🎞️ Option to create **hardcoded subtitles** directly embedded in the video.
- ⚡ Lightweight and easy to run via **Streamlit**.
- 🌍 Supports multiple languages (depending on Whisper model).

---

## 🛠️ Tech Stack

- **Frontend & UI**: [Streamlit](https://streamlit.io/)
- **Speech-to-Text**: [OpenAI Whisper](https://github.com/openai/whisper)
- **Video Processing**: [MoviePy](https://zulko.github.io/moviepy/)
- **Backend Logic**: Python 3.10+

---

## 📦 Dependencies

Make sure you have Python **3.10+** installed.  
Install the required dependencies using:

```bash
pip install -r requirements.txt
requirements.txt example:
nginx
Copy
Edit
streamlit
openai-whisper
moviepy
ffmpeg-python
torch
⚠️ You also need FFmpeg installed on your system for MoviePy to work properly.
Download: FFmpeg.org

🚀 How to Run Locally
Clone the repository


git clone https://github.com/your-username/video-subtitle-generator.git
cd video-subtitle-generator
Create and activate a virtual environment


python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
Install dependencies


pip install -r requirements.txt
Run the Streamlit app


streamlit run app.py
Open in browser
Streamlit will provide a local URL, usually:


http://localhost:8501
📂 Project Structure

video-subtitle-generator/
│
├── app.py                 # Main Streamlit app
├── dynamic_subs.py        # Subtitle rendering logic
├── requirements.txt       # Dependencies
├── README.md              # Project documentation
└── sample_videos/         # (Optional) Example videos for testing
🎬 How It Works
User uploads a video.

Audio is extracted and transcribed with Whisper.

Subtitles are generated in .srt format.

User can choose:

Download .srt file (soft subtitles).

Download video with hardcoded subtitles.

🌐 Live Demo
You can try the project live here:
👉 https://subtitlegeneratorfromvideo.streamlit.app/

📌 Future Improvements
✅ Add support for custom fonts and subtitle styling.

✅ Multi-language subtitle generation.

⏳ Speaker diarization (detect different speakers).

⏳ Export in multiple subtitle formats (.vtt, .ass).

⏳ GPU acceleration for faster transcription.

🤝 Contributing
Contributions are welcome! Feel free to fork the repo, create a feature branch, and submit a pull request.

📜 License
This project is licensed under the MIT License.

👤 Author
Aamir Lone
aamirlone004@gmail.com