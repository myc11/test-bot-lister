from requests import session
import re
import json
import discord

from utils.song import Song
from utils.requrst import *
from utils.log import Log

import traceback

title_regex = re.compile('<title data-vue-meta="true">(.*?)_哔哩哔哩_bilibili</title>')
playinfo_regex = re.compile('window.__playinfo__=(.*?)</script><script>window.__INITIAL_STATE__=', re.I | re.S)


def preprocess_bili(link):
    ses = session()
    try:
        html = ses.get(link)
        title = title_regex.findall(html.text)[0]
        return Song(title, link, source=download_bili_audio)
    except Exception as e:
        try:
            Log.log(e, 'Try searching')
            link = dragbilibili(link)
            html = ses.get(link)
            title = title_regex.findall(html.text)[0]
            return Song(title, link, source=download_bili_audio)
        except:
            traceback.print_exc()
            return None

def download_bili_audio(link):

    ffmpeg_options = {
        'before_options': f"-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -headers $\'origin:https://www.bilibili.com\r\nreferer:{link}\r\nuser-agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36\r\n\'"
    }

    ses = session()

    # Get html content
    html = ses.get(link)
    # Get name
    title = title_regex.findall(html.text)[0]

    # Find video data
    jsondata = playinfo_regex.findall(html.text)[0]
    data = json.loads(jsondata)['data']

    try:
        # New path
        base_url = data['dash']['audio'][0]['baseUrl']
    except:
        # Old path
        base_url = data['durl'][0]['url']

    source = discord.FFmpegPCMAudio(base_url, **ffmpeg_options)

    return source


if __name__ == '__main__':
    s = '123456789'
    print('134' in s)



