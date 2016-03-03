import pandas as pd
import tushare as ts 
import sqlalchemy as sqlc

route = 'sqlite:///data/stock.db'
engine = sqlc.create_engine(route)

def fetch_stock_basics():
	stock_basics = pd.read_sql('SELECT * from stock_basics', engine)
	if stock_basics.empty == True:
		stock_basics = ts.get_stock_basics()
		stock_basics.to_sql('stock_basics', engine, if_exists = 'replace')
	return stock_basics


if __name__ == '__main__':
	stock_basics = fetch_stock_basics()
	print(stock_basics)
