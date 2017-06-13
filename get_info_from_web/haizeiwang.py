#从风之动漫网站下载海贼王漫画

import os, requests, bs4

no_hua = 868

url = 'http://www.fzdm.com/manhua/02/'+str(no_hua)+'/index_0.html'
url0 = 'http://www.fzdm.com/manhua/02/'+str(no_hua)+'/'
os.makedirs('hzw/'+str(no_hua), exist_ok=True)

n = 0
nmax = 20

while n<nmax and not url.endswith('#'):
   # Download the Page
   print('Download page %s ..' % url)
   res = requests.get(url)
   res.raise_for_status()
   
   soup = bs4.BeautifulSoup(res.text,"html.parser")
   # find the URL of the comic image
   #comicElem = soup.select('#mhpic img')
   comicElem = soup.select('img[id="mhpic"]')
   print(comicElem)
   if comicElem == []:
      print('Could not find comic image.')
   else:
      comicUrl = 'http:'+ comicElem[0].get('src')
      #download the image
      print('Downloading image %s ...' % (comicUrl))
      res = requests.get(comicUrl)
      res.raise_for_status()
      #save the image to ./xkcd
      pic_prefix = 'hzw'+str(n)+"_"
      imageFile = open(os.path.join('hzw/'+str(no_hua), pic_prefix+os.path.basename(comicUrl)), 'wb')
      for chunk in res.iter_content(100000):
         imageFile.write(chunk)
      imageFile.close()
      n = n+1
   #get the prev button's url
   #prevLink = soup.select('a[rel="prev"]')[0]
   prevLink = soup.select('a[id="mhona"]')
   if prevLink==[]:
	break
   last = len(prevLink) - 1
   url = url0 + prevLink[last].get('href')
   #print('next url is %s' % url)

print('Done')
