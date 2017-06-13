
import os, requests, bs4

url = 'https://xkcd.com/'
os.makedirs('xkcd', exist_ok=True)

n = 0
nmax = 3

while n<nmax and not url.endswith('#'):
   # Download the Page
   print('Download page %s ..' % url)
   res = requests.get(url)
   res.raise_for_status()
   
   soup = bs4.BeautifulSoup(res.text)
   # find the URL of the comic image
   comicElem = soup.select('#comic img')
   if comicElem == []:
      print('Could not find comic image.')
   else:
      comicUrl = 'http:'+ comicElem[0].get('src')
      #download the image
      print('Downloading image %s ...' % (comicUrl))
      res = requests.get(comicUrl)
      res.raise_for_status()
      #save the image to ./xkcd
      imageFile = open(os.path.join('xkcd', os.path.basename(comicUrl)), 'wb')
      for chunk in res.iter_content(100000):
         imageFile.write(chunk)
      imageFile.close()

   #get the prev button's url
   n = n+1
   prevLink = soup.select('a[rel="prev"]')[0]
   url = 'http://xkcd.com' + prevLink.get('href')

print('Done')
