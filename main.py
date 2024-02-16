import os
import random
import download_videos
import create_video
import time


if __name__ == "__main__":
    if len(os.listdir('media/raw_videos')) == 0:
        download_videos.download_from_playlist()
    if len(os.listdir('media/gameplay_videos')) == 0:
        download_videos.download_gameplay_videos()
            
    random_episode = random.choice(os.listdir("./media/raw_videos"))

    starting_time = time.time()
    create_video.create_video_with_subs("./media/raw_videos/"+random_episode)
    ending_time = time.time()
    print(f"Created the video clips in {round((ending_time - starting_time),2)} seconds")

    time.sleep(5)

    create_video.delete_full_episode(random_episode)
    
    print(f"The process has finished!")