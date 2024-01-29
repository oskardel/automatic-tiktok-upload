from tiktok_uploader.upload import upload_videos
from tiktok_uploader.auth import AuthBackend
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService


def upload_clip_tiktok() -> None:
    chrome_options = Options()
    chrome_options.add_argument('--enable-chrome-browser-cloud-management')
    service = ChromeService()
    driver = webdriver.Chrome(options=chrome_options, service=service)
    auth = AuthBackend(cookies="cookies.txt")

    videos = []
    for video_clip in os.listdir("./media/finished_videos"):
        new_video = {}
        new_video["path"] = f"./media/finished_videos/{video_clip}"
        new_video["description"] = f"Código Lyoko | EP.{video_clip.split('-')[1][:2]} PARTE {int(video_clip.split('-')[0])+1} #codigolyoko #codelyoko #doblaje #doblajecastellano #castellano #infancia #fyp #fypシ #foryoupage #parati #ai #ia"
        # schedule = datetime.datetime.now() + datetime.timedelta(hours=((int(video_clip.split('-')[0])+1) * 2))

        videos.append(new_video)

    upload_videos(videos=videos, 
                  auth=auth, 
                  browser="chrome", 
                  browser_agent=driver)
            
upload_clip_tiktok()