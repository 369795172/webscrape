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