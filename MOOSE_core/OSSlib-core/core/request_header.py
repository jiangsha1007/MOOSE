import urllib3
import random

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
accept = 'application/json,application/vnd.github.mercy-preview+json'
headers = [urllib3.util.make_headers(user_agent = user_agent , basic_auth='jiangsha1007:js19851007851007'),
        urllib3.util.make_headers(user_agent = user_agent, basic_auth = 'cit-bot1:sjtucit1'),
        urllib3.util.make_headers(user_agent = user_agent, basic_auth = 'cit-bot2:sjtucit2'),
        urllib3.util.make_headers(user_agent = user_agent, basic_auth = 'cit-bot3:sjtucit3'),
        urllib3.util.make_headers(user_agent = user_agent, basic_auth = 'cit-bot4:sjtucit4'),
        urllib3.util.make_headers(user_agent = user_agent, basic_auth = 'cit-bot5:sjtucit5'),
        urllib3.util.make_headers(user_agent = user_agent, basic_auth = 'cit-bot6:sjtucit6'),
        urllib3.util.make_headers(user_agent = user_agent, basic_auth = 'cit-bot7:sjtucit7'),
        ]

for header in headers:
    header['Accept'] = accept
    #header['Authorization'] = 'token 1cdbb8bf19515589c90d50a1f802e3d92277dfb9'

def getHeader():
    return  headers[random.randint(0, len(headers)-1)]
def getHeader2():
    return  headers[random.randint(0, len(headers)-1)]