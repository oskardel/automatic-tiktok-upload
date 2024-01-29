import os
import random
import download_videos
import create_video
import add_subtitles


if __name__ == "__main__":
    if len(os.listdir('media/raw_videos')) == 0:
        download_videos.download_from_playlist()
    if len(os.listdir('media/gameplay_videos')) == 0:
        download_videos.download_gameplay_videos()
            
    random_episode = random.choice(os.listdir("./media/raw_videos"))
    create_video.create_video_without_subs("./media/raw_videos/"+random_episode)
    add_subtitles.add_subtitles_to_video()
    create_video.delete_videos()

# TODO:
# - ARREGLAR PROBLEMA FINAL VÍDEO (DURA MÁS DE LO QUE DURA EL EPISODIO DE CODIGO LYOKO) ✔
# - IMPLEMENTAR CÓDIGO PARA SUBIR AUTOMÁTICAMENTE A TIKTOK ✔
# - SUBIR A GITHUB ✖
# - CREAR EC2 EN AWS Y SUBIR EL CÓDIGO ✖