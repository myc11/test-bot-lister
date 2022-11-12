import urllib.request
import urllib.parse
import re
import urllib
async def dragyoutube(link):
    query_string = urllib.parse.urlencode({"search_query": link})
    html_content = urllib.request.urlopen("https://www.youtube.com.hk/results?" + query_string)
    search_results = re.findall(r'url\"\:\"\/watch\?v\=(.*?(?=\"))', html_content.read().decode())
    if search_results:
        nlink = "http://www.youtube.com/watch?v={}".format(search_results[0])
        return nlink
        if not os.path.isfile(download_path):
            return 'fuck you'
#async def dragbilibil(link):