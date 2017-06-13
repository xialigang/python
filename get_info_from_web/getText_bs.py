
import requests, os, bs4

def getpic(url, picdir='pic', nmax = 10):
   os.makedirs(picdir, exist_ok=True)
   print('access page: %s ...' % url)
   res = requests.get(url)
   res.raise_for_status()
   #print(res.text)
   soup = bs4.BeautifulSoup(res.text, "html.parser")
   #picElemList = soup.select('.img-container img')
   picElemList = soup.select('.article-content p')
   #picElemList = soup.select('p img')
   #print(picElem)
   n = 0
   f = open('test.txt', 'w')
   f = open('test.txt', 'a')
   for picElem in picElemList:
      if picElem == []:
         print('Could not download!')
      elif n<nmax:
         print(picElem)
         f.write(picElem.text)
         f.write('\n')
         '''
         picUrl = picElem.get('src')
         print('Downloading image %i : %s ' %(n+1, picUrl))
         res = requests.get(picUrl)
         res.raise_for_status()
         imageFile = open(os.path.join('pic', os.path.basename(picUrl)), 'wb')
         for chunk in res.iter_content(100000):
             imageFile.write(chunk)
         imageFile.close()
         '''
         n = n + 1

   return None






url = 'http://blog.csdn.net/werm520/article/details/47189761'
url = 'https://www.baidu.com/home/news/data/newspage?nid=2977654511497302246&n_type=0&p_from=1'
picdir = 'pic'
getpic(url, picdir)

