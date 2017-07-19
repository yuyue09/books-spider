import requests
from bs4 import BeautifulSoup



#该方法用来获取开始爬取的页面
def get_urls():
    session=requests.Session()
    headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",  "Accept":"text/html,application/xhtml+xml,application/xml; q=0.9,image/webp,*/*;q=0.8"}
    url='https://book.douban.com/tag/'
    req=session.get(url,headers=headers)
    url_list=[]

    try:
        soup=BeautifulSoup(req.text,'lxml')
        tags=soup.find('div',{'id':'content'}).findAll('td')
    except Exception as e:
        print('你要的信息不存在！',e)
    for tag in tags:
        tag=tag.a.get_text()
        url='https://book.douban.com/tag/'+tag
        url_list.append(url)
    return url_list


    
    


