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
    name=['连锁店名','门店名','门店曾用名','联系人','电话','地址','登记机关','邮箱']
    ##keywords setup
    output=dict()
    keywords=df['客户']
    login,host,values=login_values()
    for keyword in keywords:
        myurl="https://www.tianyancha.com/search/os2?key={}".format(keyword)
        chs_html=webscrape(login,host,values,myurl)

        chs_links=getlist(keyword,login,host,values,chs_html)

        data=scrapchs(keyword,login,host,values,chs_links)
        output.update(data) 
   

    df = pd.DataFrame(output,index=name)
    df.to_csv('csvfile.csv',encoding='utf-8')
    print("\nAll chain stores' retailers generation complete!\n You are all set!")
    return df