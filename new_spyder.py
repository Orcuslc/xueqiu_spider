# The new spyder module for xueqiu_spyder
import requests
import re
from datetime import datetime as dt
import time
import sqlite3 as sq3
import pandas as pd
import sqlalchemy as sqa
import json

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
		self.data = pd.DataFrame({
								'time':None,
								'person':None,
								'length':None,
								'retweet':None,
								'reply':None,
								'favourite':None,
								'donate_count':None,
								'donate_snowcoin':None},
								index = [code for i in range(2000)]) # in order to prevent overflow;
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

	def _get_page(self, index):
		'''Get the comments data with the index of page; The range of index should be within 1 and 100;'''
		url = 'https://xueqiu.com/statuses/search.json?count=10&comment=0&symbol=' + self._url[-8:] + '&hl=0&source=all&sort=time&page=1'
		data_list = json.loads(requests.get(url).text)["list"]
		for data in data_list:
			time = self._handle_time(data['created_at'])

	def _handle_time(self, timestamp):