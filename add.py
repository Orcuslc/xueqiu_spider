import numpy as np

def add(a, *args):
	a = a.tolist()
	for item in args:
		a.insert(0, item)
	np.save('not_yet', np.asarray(a))