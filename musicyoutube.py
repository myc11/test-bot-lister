from __future__ import unicode_literals
import youtube_dl
import urllib.request
import urllib.parse
import re
from utils.Song import *

def download_audio(link):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'E:/dcbot/youtubemp/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        return Song(link,'E:/dcbot/youtubemp/%(title)s.%(ext)s')
    except:
        query_string = urllib.parse.urlencode({"search_query": link})
        html_content = urllib.request.urlopen("https://www.youtube.com.hk/results?" + query_string)
        search_results = re.findall(r'url\"\:\"\/watch\?v\=(.*?(?=\"))', html_content.read().decode())
        if search_results:
            nlink = "http://www.youtube.com/watch?v={}".format(search_results[0])
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([nlink])
            return Song(link,'E:/dcbot/youtubemp/%(title)s.%(ext)s')
    else:
        return 'Fuck you'



download_audio('思念是一种病')
