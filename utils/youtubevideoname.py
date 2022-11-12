import json
import urllib.request
import urllib

url = 'https://www.youtube.com/watch?v=z3UYgpFNcbQ'
async def getyoutube_name(link):
    x=link.split('=')
    li = list(x)
    li.pop(0)
    st='='
    id=st.join(li)
    params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % id}
    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string

    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())
        name=data['title']
        return name
