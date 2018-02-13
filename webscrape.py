# Marvin Yuan
# date:2018/2/7

import getpass
# login stage preparation

def login_values():
    login="https://www.tianyancha.com/login"
    username = input("Please insert your username: ") 
    password = getpass.getpass("Please type in your password: ")
    #host="www.tianyancha.com"
    #store login screts
    data = {
        "username": username, 
        "password": password, 
    }
    return login,data

####################################################################
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

#####################################################################
from bs4 import BeautifulSoup


#set up html parsing function for parsing all the list links
def getlist(keyword,login_url,login_info,html_lists):
    page=1
    pagenum=10# set up maximum page num
    links=[]
    soup=BeautifulSoup(html_lists,"lxml")
    try:
        target_part=soup.find_all("div",class_="search_result_single search-2017 pb25 pt25 pl30 pr30 ")
    except AttributeError:
        print("Attempt limit reaches!!")
        raise
    else:
        try:
            for li in soup.find("div",class_="search_pager human_pager in-block").ul.find_all('li'):
                [links.append(link.find('a')['href']) for link in target_part]
                page+=1
                if page<=pagenum:
                        try:
                            nexturl=soup.find('div',class_='search_pager human_pager in-block').ul.find('li',class_='pagination-next ng-scope ').a['href'] #next page
                        except AttributeError:
                            print("{}'s links are all stored!".format(keyword))
                            return links
                        else:
                            chs_html=webscrape(login_url,login_info,nexturl)
                            soup=BeautifulSoup(chs_html,"lxml")
        except AttributeError:
            [links.append(link.find('a')['href']) for link in target_part]
            print("There is only one page")
            return links

########################################################################
import pandas as pd
import re
import json

def scrapchs(keyword,login_url,login_info,chslinks):

    file=dict()
    
    name=['连锁店名','门店名','门店曾用名','联系人','电话','地址','登记机关','邮箱']

    for chslink in chslinks:

        targethtml=webscrape(login_url,login_info,chslink)
        soup=BeautifulSoup(targethtml,"lxml") 
        titlebox=soup.find('div',class_='company_header_width ie9Style position-rel')
        companyinfo=soup.find('div',class_='baseInfo_model2017')
        #start to write in data
        
        #连锁店名
        file[name[0]]=keyword        
        
        #门店名
        try:
            retname=titlebox.find('span',class_='f18 in-block vertival-middle sec-c2',text=True).text
            print("Scraping {}".format(retname))
        except AttributeError:
            retname=="NA"
            print("Can't find {}".format(name[1]))
            pass
        file[name[1]]=retname
        
        #门店曾用名
        try:
            usedname=titlebox.find('div',class_='historyName45Bottom position-abs new-border pl8 pr8 pt4 pb4',text=True).text
        except AttributeError:
            usedname="NA"
            print("Can't find {}".format(name[2]))
            pass
        file[name[2]]=usedname
        
        #联系人
        try:
            contact=companyinfo.find('div',class_='f18 overflow-width sec-c3').a.text
        except AttributeError:
            contact="NA"
            print("Can't find {}".format(name[3]))
            pass
        file[name[3]]=contact
        
        #电话
        try:
            phone=titlebox.find('div',class_='in-block vertical-top overflow-width mr20').script.text
        except AttributeError:
            tag=titlebox.find('div',class_='in-block vertical-top overflow-width mr20')
            phone=list(set(re.findall('[0-9]+', tag.text)))
        else:
            phone="NA"
            print("Can't find {}".format(name[4]))
            pass 
        file[name[4]]=phone
        
        #地址
        try:
            address=titlebox.find('span',class_='in-block overflow-width vertical-top').text
        except AttributeError:
            address="NA"
            print("Can't find {}".format(name[5]))
            pass
        file[name[5]]=address
        
        #城市
        city=keyword[:2]
        file[name[6]]=city
        
        #邮箱
        try:
            email=titlebox.find('span',class_='in-block vertical-top overflow-width',text=True).text
        except AttributeError:
            email="NA"
            print("Can't find {}".format(name[7]))
            pass
        file[name[7]]=email
        
        with open('output.json','a', encoding='utf8') as outfile:
            json.dump(file,outfile,ensure_ascii=False)
            outfile.write(',\n')        
        

    print("{}'s retailers generation complete!".format(keyword))
    return file

######################################################################
import numpy as np
import pandas as pd

def getcsv():
    #search keywords stage preparation

    # Load the chain stores dataset
    try:
        data = pd.read_csv('chainstore.csv',encoding='utf-8')
        df=pd.DataFrame(data)
        chs=df[df["属性"] == "连锁"]
    except:
        print ("Dataset could not be loaded. Is the dataset missing?")
    ##keywords setup
    keywords=chs['客户']
    login_url,login_data=login_values()
    for keyword in keywords:
        myurl="https://www.tianyancha.com/search/os2?key={}".format(keyword)
        chs_html=webscrape(login_url,login_data,myurl)

        chs_links=getlist(keyword,login_url,login_data,chs_html)

        scrapchs(keyword,login_url,login_data,chs_links)
   
    print("\nAll chain stores' retailers generation complete!\n You are all set!")
    return 