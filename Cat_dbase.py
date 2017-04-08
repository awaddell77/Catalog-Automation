#catalog dbase 
from dbaseObject import *
from text_l import *
import time
#should have
#export category method that produces list of products in category
class Cat_dbase(Db_mngmnt):
	def __init__(self):
		self.creds = text_l('C:\\Users\\Owner\\Documents\\Important\\cat_cred2.txt')
		super().__init__(self.creds[1], self.creds[2],'hive_inventory_production', self.creds[0])
		self.__cat_contents = []
	def get_cat_contents(self):
		return self.__cat_contents
	def set_cat_contents(self, x):
		self.__cat_contents = x

	def get_product(self, p_id):
		#uses product id only\
		d = {}
		res = self.query("SELECT * from products WHERE id = \"{0}\";".format(p_id))
		if not res:
			return []
		res = list(res[0])

		columns = self.query("SHOW COLUMNS from products")
		columns = [i[0] for i in columns]
		for i in range(0, len(columns)):
			if res[i] is None:
				res[i] = ""
			d[columns[i]] = res[i]
		descriptors = self.get_descriptors(p_id)
		for i in range(0, len(descriptors)):
			val = descriptors[i][1]
			if val is None:
				val = ''
			d[descriptors[i][0]] = val.strip(' ')
		d['category_name'] = self.cat_name(d['category_id'])
		d['product type'] = self.prod_type_name(d["product_type_id"])
	def get_product_v2(self, p_id):
		d = {}
		res = self.query("SELECT name, products.id, product_descriptors.value, product_descriptors.descriptor_id  from products RIGHT JOIN product_descriptors on products.id = product_descriptors.product_id WHERE products.id ='{0}' ;".format(p_id))


		return d
	def get_descriptor_name(self, descriptor_id):
		#takes descriptor id and returns name
		d_name = self.query("SELECT name FROM descriptors WHERE id = \"{0}\"".format(descriptor_id))
		return d_name[0][0]
	def get_descriptors(self, p_id):
		#returns the product type specific descriptors as a list of tuples
		descriptors = self.query("SELECT descriptor_id, value FROM product_descriptors WHERE product_id = \"{0}\";".format(p_id))
		descriptors = self.tup_to_lst(descriptors)
		for i in descriptors:
			i[0] = self.get_descriptor_name(i[0])
		return descriptors
	def prod_type_name(self, type_id):
		type_id = self.query("SElECT name FROM product_types WHERE id = \"{0}\";".format(type_id))
		return type_id[0][0]
	def tup_to_lst(self, x):
		#turns list of tuples into list of lists
		for i in range(0, len(x)):
			x[i] = list(x[i])
		return x
	def cat_name(self, cat_id):
		cat = self.query("SELECT name, id FROM categories WHERE id = \"{0}\";".format(cat_id))
		return cat[0][0]
	def get_category_contents(self, cat_id):
		time_start = time.time()
		products = self.query("SELECT id FROM products WHERE category_id = \"{0}\";".format(cat_id))
		p_ids = [i[0] for i in products]
		results = []
		for i in p_ids:
			print("Getting information for {0}".format(i))
			product_info = self.get_product(i)
			results.append(product_info)
		self.set_cat_contents(results)
		duration = time.time() - time_start
		print("Took {0} seconds".format(duration))
		return results









	def search_prod(self, x):
		columns = self.query("SHOW COLUMNS from products")
		columns = [i[0] for i in columns]
	def result_format(self, columns,  x):
		for i in range(0, len(columns)):
			d[columns[i]] = x[i]


