
import requests
import random
import http.cookiejar
import socket

# Set up web scraping function to output the html text file
def webscrape(login_url,login_data,target_url):
    #static values preparation
    ##import header
    user_agents = [
                'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
                'Opera/9.25 (Windows NT 5.1; U)',
                'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
                'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
                "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
                "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
                ] 
    agent = random.choice(user_agents)
    #Because by insert cookie, the headers no longer required,I will just keep some.
    headers={'User-agent':agent,
            'Accept':'*/*',
             'Accept-Language':'en-US,en;q=0.9;zh-cmn-Hans',
             'Referer':login_url,
            
            }
    ##set up cookie jar
    cj = http.cookiejar.CookieJar()
    #
    # get the html file
    socket.setdefaulttimeout(20)
    s=requests.Session()
    req=s.post(login_url, data=login_data)
    res = s.get(target_url, cookies=cj,headers=headers)
    html=res.text
    s.cookies.clear()
    return html