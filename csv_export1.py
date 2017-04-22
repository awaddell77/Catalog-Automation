#export
from soupclass8 import *

def export_csv12(lst):
	results = []
	headers = list(lst[0].keys())
	results = results + headers

	for i in lst:
		item = []
		for i_2 in headers:
			item.append([i[i_2]])
		results.append(item[:])
	w_csv(results, "exported_lst.csv")
	return results

