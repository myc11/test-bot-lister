import urllib.request
import urllib.parse
import re
import urllib
from urllib.parse import quote

def dragyoutube(link):
    headers = {
        'origin': 'www.youtube.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    query_string = urllib.parse.urlencode({"search_query": link})
    html_content = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'url"\:\"\/watch\?v\=(.*?(?=\"))', html_content.read().decode())
    if search_results:
        nlink = "http://www.youtube.com/watch?v={}".format(search_results[1])
        splits = '\\'
        nlink1 = nlink.split(splits, 1)[0]
        return nlink1
        if not os.path.isfile(download_path):
            return 'fuck you'


def dragbilibili(link):
    headers = {
        'origin': 'www.bilibili.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    link=link.replace(' ','+')
    link=quote(link)
    html_content = urllib.request.urlopen("https://search.bilibili.com/all?keyword=" + link)
    search_results = re.findall(r'www.bilibili.com/video/.*?search', html_content.read().decode())
    if search_results:
        result=search_results[0].replace('?from=search','')
        return 'https://' + result
        if not os.path.isfile(download_path):
            return 'fuck you'