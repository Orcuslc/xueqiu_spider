import tushare as ts
import pandas as pd
from datetime import datetime as dt 
from get_stock_basics import pull_stock_basics

stock_basics = pull_stock_basics()
stock_codes = stock_basics['code']

