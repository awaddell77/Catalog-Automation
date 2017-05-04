#deep copy implementation for dict

def d_copy(x):
	n_dict = {}
	keys = list(x.keys())
	for i in keys:
		n_dict[i] = x[i]
	return n_dict

