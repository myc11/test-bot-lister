import urllib.request
import urllib.parse
import re
import urllib
from urllib.parse import quote

def dragyoutube(link):
    query_string = urllib.parse.urlencode({"search_query": link})
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
    links = urllib.request.Request(query_string, headers=headers)
    html_content = urllib.request.urlopen("https://www.youtube.com.hk/results?" + links)
    search_results = re.findall(r'url\"\:\"\/watch\?v\=(.*?(?=\"))', html_content.read().decode())
    if search_results:
        nlink = "http://www.youtube.com/watch?v={}".format(search_results[0])
        return nlink
        if not os.path.isfile(download_path):
            return 'fuck you'

def dragbilibili(link):
    link=link.replace(' ','+')
    link=quote(link)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
    links = urllib.request.Request(link, headers=headers)
    html_content = urllib.request.urlopen("https://search.bilibili.com/all?keyword=" + links)
    search_results = re.findall(r'www.bilibili.com/video/.*?search', html_content.read().decode())
    if search_results:
        result=search_results[0].replace('?from=search','')
        return 'https://' + result
        if not os.path.isfile(download_path):
            return 'fuck you'