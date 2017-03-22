#auto-update
from Cat_session import *
from Cat_update import *

class Asin_update:
	def __init__(self, *args):
		#database connection
		self.dbObject = Db_mngmnt(text_cred[2],text_cred[3],'asins', '192.168.5.90')
		#catalog update instance
		self.cat_update_inst = Cat_update()
		#amazon connection
		self.amazon_inst = Asin_Add_Main()
		self.__id_check_queue = []
		self.__barcode_queue = []
		self.__id_create_queue = []
		#for product Ids coupled with asins
		self.__asin_id_lst = []
	def start_up_all(self):
		self.cat_update_inst.start()
		self.amazon_inst.start()
	def get_id_queue(self):
		return self.__id_check_queue
	def set_id_queue(self,x):
		self.__id_check_queue = x
	def get_id_create_queue(self):
		return self.__id_create_queue
	def set_id_create_queue(self, x):
		self.__id_create_queue = x

	def get_barcode_queue(self):
		return self.__barcode_queue
	def set_barcode_queue(self, x):
		self.__barcode_queue = x
	def get_ids(self, table_name):
		self.set_id_queue(self.dbObject.query("SELECT * FROM {0};".format(str(table_name))))
	def remove_ids(self):
		for i in __id_check_queue:
			pass
	def db_query(self, x):
		res = ''
		resp = self.dbObject.query(x)
		return resp
	def __get_id_asin(self, p_id):
		#returns the contents of the ASIN field for a given product
		if fn_grab(cat_update_inst.url()) == str(p_id):
			while cat_update_inst.load_check():
				time.sleep(.5)
			d = cat_update_inst.descriptor_get()
			return d["ASIN"]
		elif fn_grab(cat_update_inst.url()) != str(p_id):
			self.prod_go_to(p_id)
			while cat_update_inst.load_check():
				time.sleep(.5)
			d = cat_update_inst.descriptor_get()
			return d["ASIN"]


	def __check_id_asin(self, p_id=''):
		#returns boolean
		#checks single p_id to see if it has an ASIN
		#returns False if it has no ASIN
		#returns True if it has an ASIN
		d = self.__get_id_asin(p_id)
		if d["ASIN"] == '':
			return False
		else:
			return True
		

#need method that collects product information from catalog and makes an ASIN with it













