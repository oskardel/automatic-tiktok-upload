import scrapetube
import pytube
import time


CHANNEL_LINK = "https://www.youtube.com/@CodeLyokoESP/videos"
CHANNEL_ID = "UCE0h3VQ_o9UzGoVcAapjGDA"
PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLhI5N4xKIdM-K7P4QQWbAebb6DCd3bClF"
GAMEPLAY_VIDEOS = [
    "https://www.youtube.com/watch?v=N2ZYjGosSvA",
    "https://www.youtube.com/watch?v=Z-cHTDfXWOI",
    "https://www.youtube.com/watch?v=Z8EDKiW3Bck"
]

def get_youtube_videos_links() -> list:
    all_videos = scrapetube.get_channel(CHANNEL_ID)
    video_links_list = []
    for video in all_videos:
        video_links_list.append("https://www.youtube.com/watch?v="+video["videoId"])
    return video_links_list

def download_video_youtube(link: str) -> None:
    video_link = pytube.YouTube(link)
    video_downloader = video_link.streams.get_highest_resolution()
    video_title = f'{video_downloader.title[17:19]}codigo_lyoko.mp4'
    if video_downloader.title[0] == "C":
        video_downloader.download(output_path="media/raw_videos", filename=video_title)

def download_video_playlist(playlist_url: str) -> None:
    start_time = time.time()
    playlist = pytube.Playlist(playlist_url)
    video_counter = 0

    for video_url in playlist.video_urls:
        youtube_video = pytube.YouTube(
            video_url,
            use_oauth=True,
            allow_oauth_cache=True
        )
        video_downloader = youtube_video.streams.get_highest_resolution()
        video_title = f'{str(video_counter).zfill(2)}codigo_lyoko.mp4'
        video_downloader.download(output_path="./media/raw_videos", filename=video_title)
        video_counter += 1

    end_time = time.time()
    print(f"Downloaded {video_counter} in {(end_time - start_time)}s")

def download_gameplay_videos() -> None:
    video_counter = 1
    for video in GAMEPLAY_VIDEOS:
        youtube_video = pytube.YouTube(
            video,
            use_oauth=True,
            allow_oauth_cache=True
        )

        video_downloader = youtube_video.streams.get_highest_resolution()
        video_title = f'gameplay_video{video_counter}.mp4'
        video_downloader.download(output_path="./media/gameplay_videos", filename=video_title)
        video_counter += 1

def download_from_playlist() -> None:
    download_video_playlist(PLAYLIST_URL)

def download_from_channel() -> None:
    videos_link = get_youtube_videos_links()
    for link in videos_link:
        download_video_youtube(link)