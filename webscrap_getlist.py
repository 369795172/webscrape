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