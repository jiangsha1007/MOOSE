import urllib3
import random
import requests
import traceback
import json

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
accept = 'application/vnd.github.v3+json'
Connection = 'close'
headers = [
            urllib3.util.make_headers(user_agent = user_agent, basic_auth = 'cit-bot1:sjtucit1'),
            urllib3.util.make_headers(user_agent = user_agent, basic_auth = 'cit-bot2:sjtucit2'),
            urllib3.util.make_headers(user_agent = user_agent, basic_auth = 'cit-bot3:sjtucit3'),
            urllib3.util.make_headers(user_agent = user_agent, basic_auth = 'cit-bot4:sjtucit4'),
            urllib3.util.make_headers(user_agent = user_agent, basic_auth = 'cit-bot5:sjtucit5'),
            urllib3.util.make_headers(user_agent = user_agent, basic_auth = 'cit-bot6:sjtucit6'),
            urllib3.util.make_headers(user_agent = user_agent, basic_auth = 'cit-bot7:sjtucit7')]
for header in headers:
    header['Accept'] = accept
    header['Connection'] = Connection

def getHeader():
    return headers[random.randint(0, len(headers)-1)]

def getHeader2():
    headers0 = headers[random.randint(0, len(headers)-1)]
    headers0['Accept'] = 'application/vnd.github.v3.star+json'
    return headers0

def get_html_json(url, header):
    try:
        response = requests.get(url, headers=header)
        text_info = response.text
        text_json = json.loads(text_info)
        head_info = response.headers
        return text_json, head_info
    except:
        traceback.print_exc()