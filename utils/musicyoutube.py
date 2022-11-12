import os.path
import youtube_dl
import yt_dlp
import urllib.request
import urllib.parse
import re
import urllib
import simplejson
from utils.song import *
from download import download_audio_local
from youtubevideoname import getyoutube_name
from requrst import dragyoutube

async def download_audio_local(link):
    path=download_audio_local(link)
    if path=='fuckyou':
        return path
    else:
        name= getyoutube_name(link)
        return Song(name , path, Song.LOCAL)

async def download_audio_global(link):
    try:
        ydl_opts = {'format': 'bestaudio'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            url = info['formats'][0]['url']
        name= getyoutube_name(link)
        return Song(name, url, Song.URL)
    except:
        links=dragyoutube(link)
        if link=='fuck you':
            return 'fuck you'
        else:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(links, download=False)
                url = info['formats'][0]['url']
            name=getyoutube_name(link)
            return Song(name, url, Song.URL)

