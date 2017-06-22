#preorder addition
from date_form import *

class Preorder_add:
	def __init__(self, *args):
		self.cat_inst = Cat_product_add()
		self.po_data = []
		self.dupe_check = True
		self.cat_items = []
		self.__distributors = ['GTS', 'UD', 'AGD', "N/A"]
		self.__inst_present = False
		self.__po_source = ""
	def set_po_source(self, x):
		if str(x) in self.__distributors:
			self.__po_source = str(x)
		else:
			raise AssertionError("{0} is not in list of distributors".format(str(x)))
	def start_inst(self):
		cat_inst.start()
		cat_inst.set_dupe_check(self.dupe_check)
		self.__inst_present = True
	def import_file(self, x):
		tmp = dictionarify(x)
		for i in tmp:
			check = i["Original_name"]
			check = i["Product Image"]
			check = i["Product Name"]
			check = i["Manufacturer SKU"]
			try:
				i["Year"]
			except KeyError:
				i["Year"] = str(time.localtime()[0])
		#if it isn't missing the required fields then it assigns tmp to po_data
		self.po_data = tmp

	def add_preorders(self):
		if not self.__inst_present:
			self.start_inst()
		if not po_data:
			raise RuntimeError("Did not find preorder data. Try importing a CSV first.")
		cat_inst.fname = po_data
		cat_inst.add_prod_cat_batch()
		self.cat_items = cat_inst.get_addlst()
		self.add_dbase()
		self.add_m_dbase()




	def add_dbase(self):
		columns = ['product_name', 'product_id', 'sku', 'manufacturer', 'category_id', 'date_added']
		items = self.cat_items
		for i in items:
			if i["Product Id"].isdigit():
				info = [i["Product Name"], i["Product Id"], i.get('Manufacturer SKU', ''), i.get("Manufacturer", ''), i.get("Category", ''), date_form()]
				try:
					cat_inst.dbase_add(info, columns, 'preorders','adds' )
				except:
					
					print("Failed to add {0}".format(i["Product Name"]))
				else:
					print("Added {0} to database.".format(i["Product Name"]))

	def add_m_dbase(self):
		columns = ['product_name', 'product_id', 'sku', 'manufacturer', 'date_added']
		items = self.cat_items
		dists = {'GTS': 'adds_gts' , 'UD':'adds_ud', 'AGD':'adds_agd'}


		for i in items:
			if i["Product Id"].isdigit():
				info = [i["Original_name"], i["Product Id"], i.get('Manufacturer SKU', ''), i.get("Manufacturer", ''), date_form()]
				try:
					cat_inst.dbase_add(info, columns, 'preorders', dist[self.__po_source] )
				except:
					
					print("Failed to add {0}".format(i["Product Name"]))
				else:
					print("Added {0} to database.".format(i["Product Name"]))










