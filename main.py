from new_spyder import *
import requests
import re
from datetime import datetime as dt
import time
import sqlite3 as sq3
import pandas as pd
import sqlalchemy as sqa
import json
import threading
from get_stock_basics import fetch_stock_basics
import numpy as np

url = 'https://xueqiu.com'
headers = {
			'Host': 'xueqiu.com',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
			'Accept': 'application/json, text/javascript, */*; q=0.01',
			'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
			# 'Cache-Control': 'no-cache',
			'X-Requested-With': 'XMLHttpRequest',
			'Connection': 'keep-alive'
			}
r = requests.get(url, headers = headers)
cookies = r.cookies
conn = sqa.create_engine(r'sqlite:///E:\Chuan\Documents\GitHub\xueqiu_spider\data\stock.db')

global codelist, index

codelist = np.load('not_yet.npy').tolist()
listlock = threading.RLock()

class spyder(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.thread_stop = False

	def run(self):
		global codelist
		while len(codelist) >= 1:
			listlock.acquire()
			code = codelist.pop(0)
			print ('Thread(%s) locked, Number: %s'%(self.getName(), code))
			listlock.release()
			try:
				com_spy = comment_spyder(code, conn, cookies)
				fol_spy = follower_spyder(code, conn, cookies)
				com_spy._get_data()
				fol_spy._get_data()
				com_spy._save_to_database()
				fol_spy._save_to_database()
				listlock.acquire()
				np.save('not_yet', np.asarray(codelist))
				listlock.release()
			except BaseException:
				listlock.acquire()
				codelist.append(code)
				listlock.release()
			time.sleep(3)
		print('%s Completed!'%self.getName())
		
	def stop(self):
		self.thread_stop = True	

if __name__ == '__main__':
	try:
		thread_list = []
		for i in range(4):
			thread = spyder()
			thread_list.append(thread)
		for i in range(4):
			thread_list[i].start()
	except KeyboardInterrupt:
		for i in thread_list:
			i.stop()