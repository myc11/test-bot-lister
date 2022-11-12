import os.path
import youtube_dl
import yt_dlp
from utils.song import *
from utils.requrst import dragyoutube

def download_audio_local(link):
    download_path = f'youtubemp/{link}.mp3'
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': download_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        return Song(download_path)
    except:
        links=dragyoutube(link)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([links])
        return Song(download_path)
    else:
        return 'fuckyou'