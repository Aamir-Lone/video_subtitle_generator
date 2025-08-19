from moviepy import VideoFileClip

clip = VideoFileClip("sample.mp4")  # replace with an actual file
print(f"Duration: {clip.duration} seconds")
clip.close()
