import requests
import re
# from datetime import datetime as dt
import time
# import sqlite3
import pymongo as mg 
import multiprocessing as mtp
import threading as tr 

class comment_spyder:
	'''
	The main class of spyder for stock comments
	'''
	def __init__(self, code):
		self.code = code
		self.headers = {
			# GET /statuses/search.json?count=10&comment=0&symbol=SZ000917&hl=0&source=all&sort=alpha&page=1&_=1456833666936 HTTP/1.1
			'Host': 'xueqiu.com',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
			'Accept': 'application/json, text/javascript, */*; q=0.01',
			'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
			# Accept-Encoding: gzip, deflate
			'Cache-Control': 'no-cache',
			'X-Requested-With': 'XMLHttpRequest',
			# 'Referer': 'http://xueqiu.com/S/SZ000917',
			'Cookie': 'Hm_lvt_1db88642e346389874251b5a1eded6e3=1455272909,1456817053,1456817184; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1456831074; s=1mkm1low5q; xq_a_token=fb836770b2d5ca88e71608d0c21327a306073355; xq_r_token=7eeee1f3170459bb8bcc6aa066e53cc299167093; __utma=1.503405128.1456830680.1456830680.1456833100.2; __utmc=1; __utmz=1.1456830680.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); webp=0; __utmb=1.3.10.1456833100; __utmt=1',
			'Connection': 'keep-alive'
			}
		self.today = dt.now()
		self.url = self._get_url()
		self.timestamp = None
		self.headers['Referer'] = self.url

	def _get_url(self):
		if self.code[0] in ['3', '6']:
			url = 'http://xueqiu.com/S/' + 'SZ' + self.code
		elif self.code[0] == '0':
			url = 'http://xueqiu.com/S/' + 'SH' + self.code
		else:
			raise BaseException('Failed to get url for the stock %s, Please check again' %self.code)
		return url 
	
	def _fetch_timestamp(self, count, flag = True):
		url = 'http://xueqiu.com/statuses/search.json?count=10&comment=0&symbol=' \
			+ self.url[-8:] + '&h1=0&source=all&sort=alpha&page=' + str(count)
		page = requests.get(url, headers = self.headers)
		comments = re.findall(r'"created_at":[0-9]*,', page.text)
		if comments == []:
			return [], False
		timestamp = []
		for com in comments:
			'''
			The result should be like '"created_at":1450698976000,'
			'''
			timestamp.append(int(com[-14:-4]))
		return timestamp, True

	def _handle_timestamp(self, timestamp):
		'''
			According to analysis, the DATE value of every comment in XUEQIU is created by \
		Unix standard time multiply 1000, and then processed by INT(). Hence, we can handle \
		the date by using time.localtime(date)
		'''
		format = '%Y-%m-%d %H:%M:%S'
		value = time.localtime(timestamp)
		date = time.strftime(format, value)
		'''
		date is like '2013-07-01 07:39:59'
		'''
		return date[:10]

	def get_comment_time(self):
		count = 1
		flag = True
		timestamp_list = []
		while flag == True:
			timestamp, flag = self._fetch_timestamp(count, flag)
			if flag == True:
				timestamp_list.extend(list(map(self._handle_timestamp, timestamp)))
			count += 1
		return timestamp_list

if __name__ == '__main__':
	sp = comment_spyder('000917')
	l = sp.get_comment_time()
	print(l)