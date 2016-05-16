from new_spyder import *
import requests
import re
from datetime import datetime as dt
import time
import sqlite3 as sq3
import pandas as pd
import sqlalchemy as sqa
import json


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
r = requests.get(url, headers = headers, verify = False)
cookies = r.cookies
conn = sqa.create_engine(r'sqlite:///E:\Chuan\Documents\GitHub\xueqiu_spider\data\stock.db')
c = follower_spyder('002618', conn, cookies)
c.run()