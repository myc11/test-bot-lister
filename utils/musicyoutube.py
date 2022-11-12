import os.path
import youtube_dl
import yt_dlp
import urllib.request
import urllib.parse
import re
import urllib
import simplejson
from utils.song import *

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
        json = simplejson.load(urllib.urlopen(link))
        title = json['entry']['title']['$t']
        author = json['entry']['author'][0]['name']
        name= "id:%s\nauthor:%s\ntitle:%s" % (title, author, link)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        return Song(name , download_path, Song.LOCAL)
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
            json = simplejson.load(urllib.urlopen(nlink))
            title = json['entry']['title']['$t']
            author = json['entry']['author'][0]['name']
            name = "id:%s\nauthor:%s\ntitle:%s" % (title, author, link)
            return Song(name, download_path, Song.LOCAL)

def download_audio_global(link):
    try:
        ydl_opts = {'format': 'bestaudio'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            url = info['formats'][0]['url']
        json = simplejson.load(urllib.urlopen(link))
        title = json['entry']['title']['$t']
        author = json['entry']['author'][0]['name']
        name = "id:%s\nauthor:%s\ntitle:%s" % (title, author, link)
    except:
        query_string = urllib.parse.urlencode({"search_query": link})
        html_content = urllib.request.urlopen("https://www.youtube.com.hk/results?" + query_string)
        search_results = re.findall(r'url\"\:\"\/watch\?v\=(.*?(?=\"))', html_content.read().decode())
        if search_results:
            nlink = "http://www.youtube.com/watch?v={}".format(search_results[0])
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=False)
                url = info['formats'][0]['url']
        else:
            return None

    try:
        json = simplejson.load(urllib.request.urlopen(nlink))
    except Exception as e:
        print(repr(e))

    title = json['entry']['title']['$t']
    author = json['entry']['author'][0]['name']
    print(title, author)
    name = "id:%s\nauthor:%s\ntitle:%s" % (title, author, link)
    song = Song(name, url, Song.URL)
    print(name)
    return Song(name, url, Song.URL)


