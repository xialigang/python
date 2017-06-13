
import requests, os, bs4

def getpic(url, picdir='pic', nmax = 5):
   os.makedirs(picdir, exist_ok=True)
   print('access page: %s ...' % url)
   res = requests.get(url)
   res.raise_for_status()
   print(res.text)
   soup = bs4.BeautifulSoup(res.text, "html.parser")
   #picElemList = soup.select('.img-container img')
   picElemList = soup.select('p img')
   #print(picElem)
   n = 0
   for picElem in picElemList:
      if picElem == []:
         print('Could not download!')
      elif n<nmax:
         picUrl = picElem.get('src')
         print('Downloading image %i ' %(n+1))
         res = requests.get(picUrl)
         res.raise_for_status()
         imageFile = open(os.path.join('pic', os.path.basename(picUrl)), 'wb')
         for chunk in res.iter_content(100000):
             imageFile.write(chunk)
         imageFile.close()
         n = n + 1

   return None






#url = 'https://www.baidu.com/home/news/data/newspage?nid=4309493848520255976&n_type=0&p_from=1'
#url = 'https://xkcd.com/'
#url = 'http://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&word=%E5%88%98%E4%BA%A6%E8%8F%B2'
#url = 'https://www.baidu.com/home/news/data/newspage?nid=3555630450651297766&n_type=0&p_from=1'
url = 'http://weibo.com/ttarticle/p/show?id=2309404118135618819343'
url = 'http://weibo.com/5345450769/F7sCkzHZe?ref=feedsdk&type=comment#_rnd1497325115843'
url = 'http://cnews.chinadaily.com.cn/2017-06/12/content_29709637.htm'
picdir = 'pic'
getpic(url, picdir)

