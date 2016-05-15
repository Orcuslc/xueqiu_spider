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
	def __init__(self, code, conn):
		self._code = code
		self._headers = {
			'Host': 'xueqiu.com',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
			'Accept': 'application/json, text/javascript, */*; q=0.01',
			'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
			# Accept-Encoding: gzip, deflate
			'Cache-Control': 'no-cache',
			'X-Requested-With': 'XMLHttpRequest',
			'Connection': 'keep-alive'
			}
		self._get_url()
		self._get_cookies() # get cookies before getting data in order to prevent that the request would be refused;
		self._count = 0 # the number of data;
		self.data = pd.DataFrame() 
		self._conn = conn # SQLAlchemy Engine

	def _get_cookies(self):
		'''Get the cookies for xueqiu.com'''
		url = 'http://xueqiu.com'
		r = requests.get(url, headers = self._headers)
		self._cookies = r.cookies

	def _get_url(self):
		'''Get url for the stock'''
		if self._code[0] in ['3', '0']:
			url = 'http://xueqiu.com/S/' + 'SZ' + self._code
		elif self._code[0] == '6':
			url = 'http://xueqiu.com/S/' + 'SH' + self._code
		else:
			raise BaseException('Failed to get url for the stock %s, Please check again' %self._code)
		self._url = url

	def _get_data(self):
		'''Get the comments data with the index of page; The range of index should be within 1 and 100;'''
		for index in range(1, 100):
			print(self.code, 'comment', index)
			time.sleep(0.1)
			url = 'https://xueqiu.com/statuses/search.json?count=10&comment=0&symbol=' + self._url[-8:] + '&hl=0&source=all&sort=time&page=' + str(index)
			try:
				text = requests.get(url, headers = self._headers, cookies = self._cookies).text
			except requests.exceptions.ConnectionError:
				break
			record_list = json.loads(text)["list"]
			for record in record_list:
				record['time'] = self._handle_time(record['created_at'])
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
		print('%s Started;'%self.code)
		self._get_data()
		# self.data = self.data.fillna(0.0)
		self._save_to_database()
		print('%s Ended;'%self.code)


if __name__ == '__main__':
	c = comment_spyder('000001', conn)
	c.run()