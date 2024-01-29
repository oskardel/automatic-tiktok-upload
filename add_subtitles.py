import os
from moviepy.editor import *
import whisper_timestamped
from moviepy.config import change_settings


def add_subtitles_to_video() -> None:
    change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q8\magick.exe"})
    if len(os.listdir("./media/processed_videos")) == 0:
        print("Error: there are no videos created to add subtitles")
    
    for video_clip in os.listdir("./media/processed_videos"):
        model = whisper_timestamped.load_model("medium", device="cpu")
        audio = whisper_timestamped.load_audio(f"./media/processed_videos/{video_clip}")
        clip = VideoFileClip(filename=f"./media/processed_videos/{video_clip}")

        result = whisper_timestamped.transcribe(model, audio, language="es", remove_punctuation_from_words=True)

        subtitles = []
        subtitles.append(clip)
        for segment in result["segments"]:
            for word in segment["words"]:
                text = word["text"].upper()
                start = word["start"]
                end = word["end"]
                duration = end - start
                text_clip = TextClip(txt=text, fontsize=90, font="Impact", stroke_width=5, stroke_color="black", color="white")
                text_clip = text_clip.set_start(start).set_duration(duration).set_pos("center")
                subtitles.append(text_clip)

        # POSIBLE SOLUCIÓN: hacer subclip del compositevideoclip (PROBAR)
        clip = CompositeVideoClip(clips=subtitles).subclip(0, clip.duration)
        clip.write_videofile(filename=f"./media/finished_videos/{video_clip}", fps=24)