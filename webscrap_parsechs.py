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