import time
import base64
import rsa
import math
import random
import binascii
import requests
import re

from urllib.parse import quote_plus

agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0'

headers = {
      'User-Agent': agent
      }


session = requests.session()

index_url = 'http://weibon.com/login.php'


def get_pincode_url(pcid):
   size = 0
   url = 'http://login.sina.com.cn/cgi/pin.php'
   pincode_url = '{}?r={}&s={}&p={}'.format(url, math.floor(random.random() * 100000000), size, pcid)
   return pincode_url

def get_su(username):
   username_quote = quote_plus(username)
   username_base64 = base64.b64encode(username_quote.encode('utf-8'))
   return username_base64.decode('utf-8')

#预登录获得servertime, nonce, pubkey, rsakv
def get_server_data(su):
   pre_url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su='
   pre_url = pre_url + su + '&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)&_='
   prelogin_url = pre_url + str(int(time.time() * 1000))
   pre_data_res = session.get(prelogin_url, headers=headers)

   server_data = eval(pre_data_res.content.decode('utf-8').replace('sinaSSOController.preloginCallBack',''))
   return server_data


#用户密码加密
def get_password(password, servertime, nonce, pubkey):
   rsaPublickey = int(pubkey, 16)
   key = rsa.PublicKey(rsaPublickey, 65537) #创建公钥
   message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)
   message = message.encode('utf-8')
   passwd = rsa.encrypt(message, key) #加密
   passwd = binascii.b2a_hex(passwd) #将加密信息转为16进制
   return passwd

def login(username, password):
   su = get_su(username)
   server_data = get_server_data(su)
   servertime = server_data['servertime']
   nonce = server_data['nonce']
   rsakv = server_data['rsakv']
   pubkey = server_data['pubkey']
   password_secret = get_password(password, servertime, nonce, pubkey)

   postdata = {
         'entry': 'weibo',
         'gateway': '1',
         'from': '',
         'savestate': '7',
         'useticket': '1',
         'pagerefer': 'http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl',
         'vsnf': '1',
         'su': su,
         'service': 'miniblog',
         'servertime': servertime,
         'nonce': nonce,
         'pwencode': 'rsa2',
         'rsakv': rsakv,
         'sp': password_secret,
         'sr': '1366*768',
         'encoding': 'utf-8',
         'prelt': '115',
         'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
         'returntype': 'META'
         }

   need_pin = server_data['showpin']

   print('need_pin = %i' % need_pin)

   login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
   login_page = session.post(login_url, data=postdata, headers=headers)
   login_loop = (login_page.content.decode('GBK'))
   pa = r'location\.replace\([\'"](.*?)[\'"]\)'
   loop_url = re.findall(pa, login_loop)[0]
   login_index = session.get(loop_url, headers=headers)
   uuid = login_index.text
   uuid_pa = r'"uniqueid":"(.*?)"'
   uuid_res = re.findall(uuid_pa, uuid, re.S)[0]
   web_weibo_url = 'http://weibo.com/%s/profile?topnav=1&wvr=6&is_all=1' % uuid
   weibo_page = session.get(web_weibo_url, headers = headers)
   weibo_pa = r'<title>(.*?)</title>'
   user_name = re.findall(weibo_pa, weibo_page.content.decode("utf-8", 'ignore'), re.S)[0]
   print('登录成功，你的用户名为: '+user_name)


if __name__ == '__main__':
   
   username = '13810427457'
   print('新浪用户名：'+username)
   password = input('密码：')
   login(username, password)






