from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, clips_array, CompositeVideoClip
import random
import whisper_timestamped
from moviepy.config import change_settings
import os


def create_video_with_subs(video_path: str) -> None:
    change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q8\magick.exe"})
    episode_number = int(video_path.split("/")[-1][:2])

    # Removing the intro and the outro from the original episode
    if episode_number == 0 or episode_number >= 27:
        raw_video = VideoFileClip(filename=video_path).subclip(t_start=48, t_end=-31)
    else:
        raw_video = VideoFileClip(filename=video_path).subclip(t_start=48, t_end=-13)
        
    split_points = [i * (raw_video.duration // 5) for i in range(0, 5)]
    split_points.append(raw_video.duration)

    # Creating the video transcription
    model = whisper_timestamped.load_model("medium", device="cpu")
    audio = whisper_timestamped.load_audio(video_path)
    result = whisper_timestamped.transcribe(model=model, audio=audio, language="es", remove_punctuation_from_words=True)

    for idx, point in enumerate(split_points):
        if idx >= len(split_points)-1:
            continue

        video_clip = raw_video.subclip(t_start=split_points[idx], t_end=split_points[idx+1]).resize( (720, 640) )
        raw_gameplay = VideoFileClip(filename=f"./media/gameplay_videos/{random.choice(os.listdir('media/gameplay_videos'))}")
        start_gameplay = random.randint(3, int(raw_gameplay.duration - video_clip.duration))
        gameplay_video = raw_gameplay.subclip(t_start=start_gameplay, t_end=(start_gameplay + video_clip.duration)).resize( (720, 640) )

        subtitles = []
        for segment in result["segments"]:
            for word in segment["words"]:
                text = word["text"].upper().replace("¿", "").replace("¡", "")
                start = float(word["start"] - 48.)
                end = float(word["end"] - 48.)

                # Check if the word duration overlaps with the current video clip
                if start >= split_points[idx] and end <= split_points[idx+1]:
                    texr_duration = end - start
                    text_clip = TextClip(txt=text, fontsize=80, font="Impact", stroke_width=5, stroke_color="black", color="white")
                    text_clip = text_clip.set_start(start - split_points[idx]).set_duration(texr_duration).set_pos("center")
                    subtitles.append(text_clip)

        # Combining the videos and the subtitles
        final_video = clips_array([[video_clip], [gameplay_video]])
        final_video = CompositeVideoClip([final_video] + subtitles)
        final_video.write_videofile(filename=f"./media/processed_videos/{idx}-{video_path.split('/')[-1]}")
        final_video.close()


def delete_full_episode(episode_path) -> None:
    os.remove("./media/raw_videos/"+episode_path)