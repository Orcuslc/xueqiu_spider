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
from main import *


try:
	thread_list = []
	n = 3
	for i in range(n):
		thread = spyder()
		thread_list.append(thread)
	for i in range(n):
		thread_list[i].start()
except KeyboardInterrupt:
	for i in thread_list:
		i.stop()