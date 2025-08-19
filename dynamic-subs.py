




# import cv2
# import numpy as np
# import random
# import whisper
# from PIL import ImageFont, ImageDraw, Image
# from moviepy import VideoFileClip, AudioFileClip
# import textwrap

# # Step 1: Extract transcript using Whisper
# def extract_transcript(video_path: str, model_size: str = "small") -> list:
#     model = whisper.load_model(model_size)
#     result = model.transcribe(video_path)
#     return result["segments"]  # contains text + timestamps

# # Step 2: Detect faces using OpenCV Haar Cascade
# def detect_faces(frame, face_cascade):
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(gray, 1.3, 5)
#     return faces

# # Step 3: Wrap text so it doesn’t exceed video width
# def wrap_text(text, font, max_width, draw):
#     lines = []
#     words = text.split()
#     line = ""
#     for word in words:
#         test_line = f"{line} {word}".strip()
#         bbox = draw.textbbox((0, 0), test_line, font=font)
#         line_width = bbox[2] - bbox[0]
#         if line_width <= max_width - 40:  # leave margin
#             line = test_line
#         else:
#             lines.append(line)
#             line = word
#     lines.append(line)
#     return lines

# # Step 4: Choose random position avoiding faces
# def get_text_position(frame_shape, text_size, faces):
#     h, w, _ = frame_shape
#     text_w, text_h = text_size

#     max_x = max(20, w - text_w - 20)
#     max_y = max(20, h - text_h - 20)

#     x = random.randint(20, max_x)
#     y = random.randint(20, max_y)

#     # Adjust to avoid overlapping faces
#     for (fx, fy, fw, fh) in faces:
#         if fx < x < fx + fw and fy < y < fy + fh:
#             y = fy - text_h - 10
#             y = max(20, y)

#     return x, y

# # Step 5: Render subtitles dynamically with effects
# def render_subtitles(video_path, output_path, transcript):
#     cap = cv2.VideoCapture(video_path)
#     fourcc = cv2.VideoWriter_fourcc(*"mp4v")
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     out = cv2.VideoWriter("temp_video.mp4", fourcc, fps, (width, height))

#     # Load face detector
#     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
#     font = ImageFont.truetype("arial.ttf", 32)

#     frame_num = 0
#     segment_idx = 0
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         time_sec = frame_num / fps
#         if segment_idx < len(transcript):
#             seg = transcript[segment_idx]
#             if seg["start"] <= time_sec <= seg["end"]:
#                 faces = detect_faces(frame, face_cascade)
#                 img_pil = Image.fromarray(frame)
#                 draw = ImageDraw.Draw(img_pil)

#                 # Wrap subtitle text
#                 text = seg["text"].strip()
#                 lines = wrap_text(text, font, width, draw)

#                 # Compute total block height
#                 line_heights = []
#                 max_line_w = 0
#                 for line in lines:
#                     bbox = draw.textbbox((0, 0), line, font=font)
#                     w_line = bbox[2] - bbox[0]
#                     h_line = bbox[3] - bbox[1]
#                     max_line_w = max(max_line_w, w_line)
#                     line_heights.append(h_line)
#                 text_w, text_h = max_line_w, sum(line_heights) + (len(lines) - 1) * 5

#                 pos = get_text_position(frame.shape, (text_w, text_h), faces)

#                 # Draw background box
#                 draw.rectangle(
#                     [pos, (pos[0] + text_w + 20, pos[1] + text_h + 20)],
#                     fill=(0, 0, 0, 128)
#                 )

#                 # Draw each line of text with shadow + random color
#                 y_offset = pos[1]
#                 for line, h_line in zip(lines, line_heights):
#                     draw.text((pos[0] + 3, y_offset + 3), line, font=font, fill=(0, 0, 0))
#                     draw.text(
#                         (pos[0], y_offset),
#                         line,
#                         font=font,
#                         fill=(random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)),
#                     )
#                     y_offset += h_line + 5

#                 frame = np.array(img_pil)
#             elif time_sec > seg["end"]:
#                 segment_idx += 1

#         out.write(frame)
#         frame_num += 1

#     cap.release()
#     out.release()

#     # Merge original audio back
#     video_clip = VideoFileClip("temp_video.mp4")
#     audio_clip = AudioFileClip(video_path)
#     final_clip = video_clip.with_audio(audio_clip)
#     final_clip.write_videofile(output_path, codec="libx264")

# # ---- RUN SCRIPT ----
# if __name__ == "__main__":
#     input_video = "input.mp4"       # Your input video
#     output_video = "final_output.mp4"

#     print("Extracting transcript...")
#     transcript = extract_transcript(input_video)

#     print("Rendering subtitles...")
#     render_subtitles(input_video, output_video, transcript)

#     print("✅ Done! Final video saved as", output_video)









import cv2
import numpy as np
import whisper
from PIL import ImageFont, ImageDraw, Image
from moviepy import VideoFileClip, AudioFileClip
import textwrap

# Step 1: Extract transcript using Whisper
def extract_transcript(video_path: str, model_size: str = "small") -> list:
    model = whisper.load_model(model_size)
    result = model.transcribe(video_path)
    return result["segments"]  # contains text + timestamps

# Step 2: Wrap text so it doesn’t exceed video width
def wrap_text(text, font, max_width, draw):
    lines = []
    words = text.split()
    line = ""
    for word in words:
        test_line = f"{line} {word}".strip()
        bbox = draw.textbbox((0, 0), test_line, font=font)
        line_width = bbox[2] - bbox[0]
        if line_width <= max_width - 60:  # leave margin
            line = test_line
        else:
            lines.append(line)
            line = word
    lines.append(line)
    return lines

# Step 3: Render subtitles fixed at bottom-center
def render_subtitles(video_path, output_path, transcript):
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter("temp_video.mp4", fourcc, fps, (width, height))

    # Font setup
    font = ImageFont.truetype("arial.ttf", 40)

    frame_num = 0
    segment_idx = 0
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

                # Wrap subtitle text
                text = seg["text"].strip()
                lines = wrap_text(text, font, width, draw)

                # Compute block size
                line_heights = []
                max_line_w = 0
                for line in lines:
                    bbox = draw.textbbox((0, 0), line, font=font)
                    w_line = bbox[2] - bbox[0]
                    h_line = bbox[3] - bbox[1]
                    max_line_w = max(max_line_w, w_line)
                    line_heights.append(h_line)
                text_w, text_h = max_line_w, sum(line_heights) + (len(lines) - 1) * 5

                # Fixed position: bottom-center
                x = (width - text_w) // 2
                y = height - text_h - 60

                # Draw background box
                draw.rectangle(
                    [x - 15, y - 10, x + text_w + 15, y + text_h + 10],
                    fill=(0, 0, 0, 180)
                )

                # Draw each line of text (white with black shadow)
                y_offset = y
                for line, h_line in zip(lines, line_heights):
                    # shadow
                    draw.text((x + 2, y_offset + 2), line, font=font, fill=(0, 0, 0))
                    # main text
                    draw.text((x, y_offset), line, font=font, fill=(255, 255, 255))
                    y_offset += h_line + 5

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
    final_clip = video_clip.with_audio(audio_clip)
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

# ---- RUN SCRIPT ----
if __name__ == "__main__":
    input_video = "input.mp4"       # Your input video
    output_video = "final_output.mp4"

    print("Extracting transcript...")
    transcript = extract_transcript(input_video)

    print("Rendering subtitles...")
    render_subtitles(input_video, output_video, transcript)

    print("✅ Done! Final video saved as", output_video)
