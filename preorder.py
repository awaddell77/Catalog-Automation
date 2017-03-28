from Cat_session import *

class Preorder:
	def __init__(self, fname):
		self.fname = fname
		self.cat_inst = Cat_product_add()
		self.cat_inst.start()
	def get_fname(self):
		return self.fname
	def set_fname(self, x):
		self.fname = x


	def add_pos(self):
		#adds items and then adds the entries to the preorder database
		#self.cat_inst.start()
		self.cat_inst.add_prod_cat_batch(self.fname)
		items = self.cat_inst.get_addlst()
		columns = ['product_name', 'product_id', 'sku', 'manufacturer', 'category_id', 'date_added']

		for i in items:
			if i["Product Id"].isdigit():
				info = [i["Product Name"], i["Product Id"], i.get('Manufacturer SKU', ''), i.get("Manufacturer", ''), i.get("Category", ''), date_form()]
				try:
					self.cat_inst.dbase_add(info, columns, 'preorders','adds' )
				except:
					
					print("Failed to add {0}".format(i["Product Name"]))
	def add_entries(self):
		columns = ['product_name', 'product_id', 'sku', 'manufacturer', 'category_id', 'date_added']
		items = dictionarify(self.fname)

		for i in items:
			info = [i["Product Name"], i.get("Product Id", '0000000'), i.get('Manufacturer SKU', ''), i.get("Manufacturer", ''), i.get("Category", ''), date_form()]
			try:
				self.cat_inst.dbase_add(info, columns, 'preorders','adds' )
			except:
				
				print("Failed to add {0}".format(i["Product Name"]))


