import pandas as pd
import re

def scrapchs(keyword,login,host,values,chslinks):

    file=dict()
    name=['连锁店名','门店名','门店曾用名','联系人','电话','地址','登记机关','邮箱']

    for chslink in chslinks:

        targethtml=webscrape(login,host,values,chslink)
        soup=BeautifulSoup(targethtml,"lxml") 
        titlebox=soup.find('div',class_='company_header_width ie9Style position-rel')
        companyinfo=soup.find('div',class_='baseInfo_model2017')
        try:
            file[name[0]]=keyword#连锁店名
        except AttributeError:
            file[name[0]]=""
            print("Can't find {}".format(name[0]))
            pass
        try:
            file[name[1]]=titlebox.find('span',class_='f18 in-block vertival-middle sec-c2',text=True).text#门店名
            print("Scraping {}".format(file[name[1]]))
        except AttributeError:
            file[name[1]]=""
            print("Can't find {}".format(name[1]))
            pass        
        try:
            file[name[2]]=titlebox.find('div',class_='historyName45Bottom position-abs new-border pl8 pr8 pt4 pb4',text=True).text#门店曾用名
        except AttributeError:
            file[name[2]]=""
            print("Can't find {}".format(name[2]))
            pass
        try:
            file[name[3]]=companyinfo.find('div',class_='f18 overflow-width sec-c3').a.text#联系人
        except AttributeError:
            file[name[3]]=""
            print("Can't find {}".format(name[3]))
            pass        
        try:#电话
            if type(titlebox.find('div',class_='in-block vertical-top overflow-width mr20').script)==None:
                try:
                    tag=titlebox.find('div',class_='in-block vertical-top overflow-width mr20')
                    file[name[4]]=set(re.findall('[0-9]+', tag.text))
                except AttributeError:
                    file[name[4]]=""
                    print("Can't find {}".format(name[4]))
                    pass
            else:
                file[name[4]]=titlebox.find('div',class_='in-block vertical-top overflow-width mr20').script.text            
        except AttributeError:
            file[name[4]]=""
            print("Can't find {}".format(name[4]))
            pass        
        try:
            file[name[5]]=titlebox.find('span',class_='in-block overflow-width vertical-top').text#地址
        except AttributeError:
            file[name[5]]=""
            print("Can't find {}".format(name[5]))
            pass        
        try:
            file[name[6]]=keyword[:2]#登记机关
        except AttributeError:
            file[name[6]]=""
            print("Can't find {}".format(name[6]))
            pass        
        try:
            file[name[7]]=titlebox.find('span',class_='in-block vertical-top overflow-width',text=True).text#邮箱
        except AttributeError:
            file[name[7]]=""
            print("Can't find {}".format(name[7]))
            pass
        

    print("{}'s retailers generation complete!".format(keyword))
    return file