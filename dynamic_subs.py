
import cv2
import numpy as np
import whisper
import random
from PIL import ImageFont, ImageDraw, Image
from moviepy.editor import VideoFileClip, AudioFileClip


# -----------------------------
# Step 1: Extract transcript
# -----------------------------
def extract_transcript(video_path: str, model_size: str = "small") -> list:
    model = whisper.load_model(model_size)
    result = model.transcribe(video_path)
    return result["segments"]  # contains text + timestamps


# -----------------------------
# Step 2: Subtitle Renderer (One-line only)
# -----------------------------
def render_subtitles(video_path, output_path, transcript, dynamic_colors=True):
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter("temp_video.mp4", fourcc, fps, (width, height))

    # Font setup
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 44)
    except:
        font = ImageFont.truetype("arial.ttf", 44)

    frame_num, segment_idx = 0, 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        time_sec = frame_num / fps
        if segment_idx < len(transcript):
            seg = transcript[segment_idx]
            if seg["start"] <= time_sec <= seg["end"]:
                img_pil = Image.fromarray(frame)
                draw = ImageDraw.Draw(img_pil)

                # Progressive words: calculate fraction of segment time
                seg_duration = seg["end"] - seg["start"]
                progress = (time_sec - seg["start"]) / seg_duration
                words = seg["text"].strip().split()
                word_count = max(1, int(len(words) * progress))
                current_text = " ".join(words[:word_count])

                # --- ONE LINE ONLY ---
                max_width = int(width * 0.85)
                while draw.textlength(current_text, font=font) > max_width and len(current_text.split()) > 1:
                    # Drop a word from the start to fit in one line
                    current_text = " ".join(current_text.split()[1:])

                text_w = draw.textlength(current_text, font=font)
                text_h = font.size + 10

                # Always place at bottom
                x = (width - text_w) // 2
                y = height - text_h - 60

                # Subtitle color
                if dynamic_colors:
                    color = tuple(random.randint(180, 255) for _ in range(3))
                else:
                    color = (255, 255, 255)

                # Draw outline for visibility
                for ox, oy in [(-2,0),(2,0),(0,-2),(0,2)]:
                    draw.text((x+ox, y+oy), current_text, font=font, fill=(0,0,0))

                # Draw main text
                draw.text((x, y), current_text, font=font, fill=color)

                frame = np.array(img_pil)

            elif time_sec > seg["end"]:
                segment_idx += 1

        out.write(frame)
        frame_num += 1

    cap.release()
    out.release()

    # Merge original audio back
    video_clip = VideoFileClip("temp_video.mp4")
    audio_clip = AudioFileClip(video_path)
    # final_clip = video_clip.with_audio(audio_clip)
    final_clip = video_clip.set_audio(audio_clip)

    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")


# -----------------------------
# Step 3: Save transcript to SRT
# -----------------------------
def save_srt(transcript, srt_path="subtitles.srt"):
    def format_time(seconds):
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ms = int((seconds - int(seconds)) * 1000)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"

    with open(srt_path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(transcript, 1):
            start = format_time(seg["start"])
            end = format_time(seg["end"])
            text = seg["text"].strip()
            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")


# -----------------------------
# Run script
# -----------------------------
if __name__ == "__main__":
    input_video = "input.mp4"
    output_video = "final_output.mp4"

    print("Extracting transcript...")
    transcript = extract_transcript(input_video)

    print("Saving transcript to subtitles.srt ...")
    save_srt(transcript, "subtitles.srt")

    print("Rendering subtitles...")
    render_subtitles(input_video, output_video, transcript, dynamic_colors=False)

    print("✅ Done! Final video saved as", output_video)
