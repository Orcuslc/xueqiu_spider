from get_stock_basics import fetch_stock_basics
import threading
import time
from spyder import comment_spyder, follower_spyder
from pymongo import MongoClient

global db, codelist

client = MongoClient()
db = client['stock_database']
db['comment'].remove()
db['follower'].remove()
db['count'].remove()
codelist = list(fetch_stock_basics()['code'])
listlock = threading.RLock()

class spyder(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.thread_stop = False

	def run(self):
		global codelist
		while not self.thread_stop and len(codelist) >= 1:
			listlock.acquire()
			code = codelist.pop()
			print ('Thread(%s) locked, Number: %s'%(self.getName(), code))  
			listlock.release()
			com_spy = comment_spyder(code, db)
			fol_spy = follower_spyder(code, db)
			com_spy.save_to_db()
			fol_spy.save_to_db()
			time.sleep(5)
		print('%s Completed!'%self.getName())

	def stop(self):
		self.thread_stop = True

if __name__ == '__main__':
	thread_list = []
	for i in range(4):
		thread = spyder()
		thread_list.append(thread)
	for i in range(4):
		thread_list[i].start()
			

	
