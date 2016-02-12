# import tushare as ts
# import pandas as pd
# from datetime import datetime as dt 
from get_stock_basics import pull_stock_basics
import requests
import re
from datetime import datetime as dt 
import sqlite3

stock_basics = pull_stock_basics()
# print(stock_basics)
stock_codes = stock_basics['code']

# class stock:
# 	def __init__(code):
# 		self.code = code
# 		self.new_comment = 0
# 		self.new_follows = 0
# 		self.total_comment = 0
# 		self.total_follows = 0
# 		if self.code[0] in ['3', '0']:
# 			self._url = 'http://xueqiu.com/S/' + 'SZ' + self.code
# 		elif self.code[0] == '6':
# 			self._url = 'http://xueqiu.com/S/' + 'SH' + self.code
# 		else:
# 			raise Exception('Failed to get url for the stock %s, Please check again', %self.code)
# 		# self._page = None
# 		# self._fetch_page()
# 		self._headers = {
# 		# GET /S/SZ300001 HTTP/1.1
# 		'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
# 		'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3',
# 		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.14257',
# 		# 'Accept-Encoding': 'gzip, deflate',
# 		'DNT': 1,
# 		'Host': 'xueqiu.com',
# 		'Connection': 'Keep-Alive'
# 		}

# 	# def _fetch_page(self):
# 	# 	headers = {
# 	# 	# GET /S/SZ300001 HTTP/1.1
# 	# 	'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
# 	# 	'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3',
# 	# 	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.14257',
# 	# 	# 'Accept-Encoding': 'gzip, deflate',
# 	# 	'DNT': 1,
# 	# 	'Host': 'xueqiu.com',
# 	# 	'Connection': 'Keep-Alive'
# 	# 	}
# 	# 	url = self._url + '/follows'
# 	# 	self._page = requests.get(self._url, headers = headers)

# 	def fetch_comment(self):

# 	def fetch_follows(self):
# 		url = self._url + '/follows'
# 		page = requests.get(url, headers = self._headers)
# 		follows = re.findall(r'的粉丝\([0-9]*\)人', page.text)
# 		# Notice: the result are like ['的粉丝(*****)人']
# 		self.total_follows = int(follows[0][4:][:-2])

headers = {
# GET /S/SZ300001 HTTP/1.1
	'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
	'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.14257',
	# 'Accept-Encoding': 'gzip, deflate',
	'DNT': 1,
	'Host': 'xueqiu.com',
	'Connection': 'Keep-Alive'
}

now = dt.now()
year = str(now.year)
month = str(now.month)
day = str(now.month.day)
date = year + '-' + month + '-' + day

def get_url(code):
	if code[0] in ['3', '0']:
	url = 'http://xueqiu.com/S/' + 'SZ' + code
	elif code[0] == '6':
	url = 'http://xueqiu.com/S/' + 'SH' + code
	else:
		raise Exception('Failed to get url for the stock %s, Please check again', %code)
	return url 

def fetch_follows():
	conn = sqlite3.connect('/data/stock.db')
	cursor = conn.cursor()
	for code in stock_codes:
		url = get_url(code) + '/follows'
		page = requests.get(url, headers = headers)
		follows = re.findall(r'的粉丝\([0-9]*\)人', page.text)
	# Notice: result is like ['的粉丝(*****)人']
		follows = int(follows[0][4:][:-2])
		cursor.execute('insert into stock_follows values(?, ?, ?)', code, date, follows)
	cursor.commit()
	conn.close()

def fetch_comments():
	conn = sqlite3.connect('/data/stock.db')
	cursor = conn.cursor()
	for code in stock_codes:
		url = 'http://xueqiu.com/k?q=' + code
		page = requests.get(url, headers = headers)
		comments = re.findall(r'<b id="searchResult" style="color:#BC2931">[0-9]*</b>条', page.text)
	# Notice: result is like ['<b id="searchResult" style="color:#BC2931">(****)</b>条']
		comments = int(comments[0][43:][:-5])
		cursor.execute('insert into stock_comments values(?, ?, ?)', code, date, comments)
	cursor.commit()
	conn.close()

def get_data():
	fetch_follows()
	fetch_comments()