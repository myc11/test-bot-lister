import os.path

import discord
import youtube_dl
import yt_dlp
import urllib.request
import urllib.parse
import re
import urllib
import simplejson
from utils.song import *
from utils.download import download_audio_local
from utils.youtubevideoname import getyoutube_name
from utils.requrst import dragyoutube

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
}

def download_audio_local(link):
    path=download_audio_local(link)
    if path=='fuckyou':
        return path
    else:
        name= getyoutube_name(link)
        source = discord.FFmpegPCMAudio(path)
        return Song(name, source, path)

def download_audio_global(link):
    try:
        ydl_opts = {'format': 'bestaudio'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            url = info['formats'][0]['url']
        name= getyoutube_name(link)
        source = discord.FFmpegPCMAudio(url, **ffmpeg_options)
        return Song(name, source)
    except:
        links=dragyoutube(link)
        if link=='fuck you':
            return 'fuck you'
        else:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(links, download=False)
                url = info['formats'][0]['url']
            name=getyoutube_name(link)
            source = discord.FFmpegPCMAudio(url, **ffmpeg_options)
            return Song(name, source)

