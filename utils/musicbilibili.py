from requests import session
import re
session = session()

html = session.get('https://www.bilibili.com/video/BV1qv411B7qH/')



print(html.text)


