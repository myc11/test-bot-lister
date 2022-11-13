import traceback
import discord
import youtube_dl

from utils.song import *
from utils.download import download_audio_local
from utils.youtubevideoname import getyoutube_name
from utils.requrst import dragyoutube
from utils.log import Log


def preprocess_youtube(link):
    try:
        title= getyoutube_name(link)
        return Song(title, link, Song.BILI)
    except Exception as e:
        try:
            Log.log(e, 'Try searching')
            link = dragyoutube(link)
            title= getyoutube_name(link)
            return Song(title, link, Song.BILI)
        except:
            traceback.print_exc()
            return None

def download_audio_local(link):
    path=download_audio_local(link)
    if path=='fuckyou':
        return path
    else:
        source = discord.FFmpegPCMAudio(path)
        return source

def download_audio_global(link):
    ffmpeg_options = {
        'before_options': f'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -headers $\'origin:https://www.youtube.com\r\nreferer:{link}\r\nuser-agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36\r\n\''
    }
    try:

        ydl_opts = {'format': 'bestaudio'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            url = info['formats'][0]['url']
        source = discord.FFmpegPCMAudio(url, **ffmpeg_options)
        return source
    except:
        links=dragyoutube(link)
        if link=='fuck you':
            return 'fuck you'
        else:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(links, download=False)
                url = info['formats'][0]['url']
            source = discord.FFmpegPCMAudio(url, **ffmpeg_options)
            return source

