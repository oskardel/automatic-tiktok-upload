from moviepy.editor import *
import random
import os


def create_video_without_subs(video_path: str) -> None:
    episode_number = int(video_path.split("/")[-1][:2])
    if episode_number == 0 or episode_number >= 27:
        raw_video = VideoFileClip(filename=video_path).subclip(t_start=48, t_end=-31)
    else:
        raw_video = VideoFileClip(filename=video_path).subclip(t_start=48, t_end=-13)

    split_points = [i * (raw_video.duration // 5) for i in range(0, 5)]
    split_points.append(raw_video.duration)

    for idx, point in enumerate(split_points):
        if idx >= len(split_points)-1:
            continue

        video_clip = raw_video.subclip(t_start=split_points[idx], t_end=split_points[idx+1])
        raw_gameplay = VideoFileClip(filename=f"./media/gameplay_videos/{random.choice(os.listdir('media/gameplay_videos'))}")

        start_gameplay = random.randint(3, int(raw_gameplay.duration - video_clip.duration))
        gameplay_video = raw_gameplay.subclip(t_start=start_gameplay, t_end=(start_gameplay + video_clip.duration))
        
        video_clip = video_clip.resize( (720, 640) )
        gameplay_video = gameplay_video.resize( (720, 640) )
        
        final_video = clips_array([[video_clip], [gameplay_video]])

        final_video.write_videofile(filename=f"./media/processed_videos/{idx}-{video_path.split('/')[-1]}")

def delete_videos() -> None:
    for video in os.listdir("./media/processed_videos"):
        os.remove("./media/processed_videos/"+video)