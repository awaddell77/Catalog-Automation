from Cat_session import *


def sku_grab(x):
	time.clock()
	skus = []
	p_file = C_sort(x)
	h = ['English, MTGNM','MTGNM, English','MTGNM,English', 'MTGNM']
	p_ids = p_file.col_grab(0)
	for i in range(1, len(p_ids)):
		print("Processing {0}".format(p_ids[i]))
		print("#{0} of #{1}".format(i, len(p_ids)))
		try:
			test_inst.prod_go_to(p_ids[i])
		except:
			skus.append(("Could not find", p_ids[i]))
		else:
			site = test_inst.source()
			table = site.find('table', {'class':'skus table table-condensed'})
			rows = table.find_all('tr')
			for i_2 in range(0, len(rows)):
				if rows[i_2].td.text in h:
					prod_name = site.find('h2',{'class':'product_name'}).text
					sku = rows[i_2].td.find_next().text
					skus.append((prod_name, p_ids[i], sku))
	w_csv(skus)
	print("Process took {0} seconds".format(time.clock()))
	return skus








