import numpy as np
# from degree import Frequence, supportDegree, Apriori
import pandas as pd
import matplotlib.pyplot as plt

def fwrite(x,f):
	if not x: return 
	f.write("freqset of size " + str(len(x[0])))
	for i in x:
		f.write(str(i)+"\n")
	f.write("\n")

def canConnect(l1,l2):
	if len(l1) != len(l2):
		return False
	elif l1[:-1] != l2[:-1]:
		return False
	elif l1[-1] == l2[-1]:
		return False
	else: return True

def connect(l1,l2):
	return l1[:-1] + [min(l1[-1],l2[-1])] + [max(l1[-1],l2[-1])]

def ifSubsetFrequent(candidate,freqsets):
	for i in range(len(candidate)-2):
		copy = [x for x in candidate]
		del copy[i]
		if not copy in freqsets:
			return False
	return True

def if_in_line(fs,line):
	for x in fs:
		if not x in line:
			return False
	return True	

def Frequence(data):
	degree = np.zeros(700000,dtype=np.int)
	for x in data:
		degree[x] += 1
	return degree

def supportDegree(freqset, data):
	total = len(data)
	s = 0
	for line in data:
		if if_in_line(freqset, line):
			s += 1
	return float(s)/total 


def Apriori(data, min_support):
	m = data.size
	degree = Frequence(data)
	# print(np.max(degree/m))
	freqsets_list=[]
	freqsets_list.append([[i] for i in range(1,len(degree)) if degree[i]>=min_support*m])
	while(len(freqsets_list[-1]) > 1):
		freq_i_minus_1 = freqsets_list[-1]
		l = len(freq_i_minus_1)
		#print(l)
		freq_i = []
		for u in range(l):
			for v in range(u+1, l):
				if canConnect(freq_i_minus_1[u], freq_i_minus_1[v]):
					candidate = connect(freq_i_minus_1[u], freq_i_minus_1[v])
					if ifSubsetFrequent(candidate, freq_i_minus_1):
						if supportDegree(np.array(candidate),data) >= min_support:
							freq_i.append(candidate)
							print("candidate",candidate)
		freqsets_list.append(freq_i)
	return freqsets_list

if __name__ == '__main__':
	# stock = pd.read_csv("stock.txt",\
	# 				header=None,sep="|",\
	# 				names=["id","stock_id","price","user_id","date"])
	# print("file readed")

	# total_record = len(stock)
	# stock_num = len(set(list(stock["stock_id"])))
	# user_num = len(set(list(stock["user_id"])))
	# print(total_record,stock_num,user_num)

	# follower = {}
	# for user in stock["user_id"]:
	# 	follower[user] = set()
	# print("dict bulided")

	# print("begin to bulid follow list")
	# degree = 10
	# for i in range(len(stock)):
	# 	per = float(i)/total_record * 100
	# 	if per > degree:
	# 		print(degree,"% done")
	# 		degree += 5
	# 	user, s = stock["user_id"][i], stock["stock_id"][i]
	# 	follower[user] |= set([s])    
		
	# for user in stock["user_id"]:
	# 	follower[user] = list(follower[user])
	# 	follower[user].sort()
	# print("list builded")

	# num=[]
	# for i in follower:
	# 	num.append(len(follower[i]))
	# small = []
	# large = []
	# for i in num:
	# 	if i<=8: small.append(i)
	# 	else: large.append(i)
	# # plt.hist(large)
	# # plt.show()

	# data = []
	# for i in follower:
	# 	if len(follower[i]) > 8:
	# 		data.append(follower[i])
	# data = np.array(data)
	# np.save('data', data)
	data = np.load('data.npy')
	# print(sum([len(i) for i in data]))
	print("begin to Apriori")
	freqsets_list = Apriori(data, 0.0166)

	f = open("result.txt","w")
	f.write(str(sum([len(line) for line in freqsets_list]))+"\n")
	f.write("\n")
	for i in freqsets_list:
		fwrite(i,f)
	f.close()
