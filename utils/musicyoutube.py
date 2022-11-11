import os.path

import yt_dlp
import urllib.request
import urllib.parse
import re
from utils.song import *

async def download_audio(link):
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
        return Song(link, download_path)
    except:
        query_string = urllib.parse.urlencode({"search_query": link})
        html_content = urllib.request.urlopen("https://www.youtube.com.hk/results?" + query_string)
        search_results = re.findall(r'url\"\:\"\/watch\?v\=(.*?(?=\"))', html_content.read().decode())
        if search_results:
            nlink = "http://www.youtube.com/watch?v={}".format(search_results[0])
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([nlink])
            if not os.path.isfile(download_path):
                return None
            return Song(link, download_path)
    else:
        return None

if __name__ == '__main__':

    download_audio('思念是一种病')
