# The new spyder module for xueqiu_spyder
import requests
import re
from datetime import datetime as dt
import time
import sqlite3 as sq3
import pandas as pd
import sqlalchemy as sqa
import json

conn = sqa.create_engine(r'sqlite:///E:\Chuan\Documents\GitHub\xueqiu_spider\data\stock.db')

class comment_spyder:
	'''The class of spyder for comments'''
	def __init__(self, code, conn, cookies):
		self._code = code
		self._headers = {
			'Host': 'xueqiu.com',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
			'Accept': 'application/json, text/javascript, */*; q=0.01',
			'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
			'Cache-Control': 'no-cache',
			'X-Requested-With': 'XMLHttpRequest',
			'Connection': 'keep-alive'
			}
		self._get_url()
		# self._get_cookies() # get cookies before getting data in order to prevent that the request would be refused;
		# self._count = 0 # the number of data;s
		self.data = pd.DataFrame()
		self._conn = conn # SQLAlchemy Engine
		self._headers["Referer"] = self._url
		self._cookies = cookies



	def _get_url(self):
		'''Get url for the stock'''
		if self._code[0] in ['3', '0']:
			url = 'https://xueqiu.com/S/' + 'SZ' + self._code
		elif self._code[0] == '6':
			url = 'https://xueqiu.com/S/' + 'SH' + self._code
		else:
			raise BaseException('Failed to get url for the stock %s, Please check again' %self._code)
		self._url = url

	def _get_data(self):
		'''Get the comments data with the index of page; The range of index should be within 1 and 100;'''
		for index in range(1, 3):
			print(self._code, 'comment', index)
			time.sleep(0.1)
			url = 'https://xueqiu.com/statuses/search.json?count=10&comment=0&symbol=' + self._url[-8:] + '&hl=0&source=all&sort=time&page=' + str(index)
			try:
				text = requests.get(url, headers = self._headers, cookies = self._cookies, verify = False).text
			except requests.exceptions.ConnectionError:
				break
			record_list = json.loads(text)["list"]
			for record in record_list:
				record['time'] = self._handle_time(record['created_at'])
				for key in record['user']:
					record[str('user_'+key)] = record['user'][key]
				record['user'] = str(record['user'])
				record['retweeted_status'] = str(record['retweeted_status'])
				record = pd.Series(record)
				record.name = self._code
				self.data = self.data.append(record)


	def _handle_time(self, timestamp):
		'''The timestamp in record should be like
			1450698976000, which is, according to analysis, created by The Unix Standard Time * 1000, then process by int()'''
		time_format = '%Y-%m-%d %H:%M:%S'
		timestamp = int(timestamp/1000)
		value = time.localtime(timestamp)
		date = time.strftime(time_format, value)
		return date[:10] # date is like '2013-07-01 07:39:59'
	
	def _save_to_database(self):
		self.data.to_sql('stock_comments', self._conn, if_exists = 'replace')

	def run(self):
		print('%s Started;'%self._code)
		self._get_data()
		# self.data = self.data.fillna(0.0)
		self._save_to_database()
		print('%s Ended;'%self._code)

class follower_spyder(comment_spyder):
	def __init__(self, code, conn, cookies):
		super().__init__(code, conn, cookies)
		self.trading_data = pd.DataFrame()

	def _get_data(self):
		# self._headers["referer"] = self._url
		# self._cookies = requests.get(self._url, headers = self._headers, cookies = self._cookies, verify = False).cookies
		for index in range(1, 2):
			print(self._code, 'follower', index)
			time.sleep(0.1)
			url = 'https://xueqiu.com/statuses/search.json?count=10&comment=0&symbol=' + self._url[-8:] + '&hl=0&source=trans&page=' + str(index)
			try:
				r = requests.get(url, headers = self._headers, cookies = self._cookies, verify = False)
				if r.status_code == 301:
					r = requests.get(url, headers = self._headers, cookies = self._cookies, verify = False)
				else:
					text = r.text
			except requests.exceptions.ConnectionError:
				break
			record_list = json.loads(text)["list"]
			for record in record_list:
				record['time'] = self._handle_time(record['created_at'])
				for key in record['user']:
					record[str('user_'+key)] = record['user'][key]
				record['user'] = str(record['user'])
				record['retweeted_status'] = str(record['retweeted_status'])
				a = record['text']
				if a[0] not in [i for i in range(10)]:
					try:
						price = re.findall(r'当前价 [0-9]+\.[0-9]+', a)
						price = price[0][3:]
					except BaseException:
						price = 0.0
					record["follow_price"] = str(price)
					record["sold_price"] = record["bought_price"] = 0.0
					record = pd.Series(record)
					record.name = self._code
					self.data.append(record)
				else:
					price = re.findall(r'￥[0-9]+.[0-9]+买入', a)
					if price != []:
						record["bought_price"] = price[0][1:-2]
						record["sold_price"] = 0.0
					else:
						price = re.findall(r'￥[0-9]+.[0-9]+卖出', a)
						if price != []:
							record["sold_price"] = price[0][1:-2]
							record["bought_price"] = 0.0
						else:
							price = 0.0
							record["sold_price"] = record["bought_price"] = price
					
					record["follow_price"] = 0.0
					record = pd.Series(record)
					record.name = self._code
					self.trading_data.append(record)

	def _save_to_database(self):
		self.data.to_sql('stock_followers', self._conn, if_exists = 'replace')
		self.trading_data.to_sql('stock_tradings', self._conn, if_exists= 'replace')

	def run(self):
		self._get_data()
		self._save_to_database()

if __name__ == '__main__':
	c = follower_spyder('002618', conn)
	c.run()