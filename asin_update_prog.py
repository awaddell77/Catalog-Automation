#auto-update
from Cat_session import *
from Cat_update import *
from amazon_new import *
from Amazon_list_format import *

class Asin_update:
	def __init__(self, *args):
		#database connection
		self.dbObject = Db_mngmnt(text_cred[2],text_cred[3],'asins', '192.168.5.90')
		#catalog update instance
		self.cat_update_inst = Cat_update()
		#amazon connection
		self.amazon_inst = Asin_create()
		#product information
		self.__prod_info = []
		self.__id_check_queue = []
		self.__barcode_queue = []
		self.__id_create_queue = []
		#for product Ids coupled with asins
		self.__asin_id_lst = []
		#used for start_up_all method
		self.__amazon_online = False
	def start_up_all(self):
		self.cat_update_inst.start()
		self.amazon_inst.start()
		amazon_counter = time.time()
		while not self.__amazon_online:
			if self.amazon_inst.url() in ["https://sellercentral.amazon.com/gp/homepage.html?", "https://sellercentral.amazon.com/gp/homepage.html/ref=ag_home_logo_xx"]:
				self.__amazon_online = True
				break
			elif (time.time() - amazon_counter) >= 30:
				raise RuntimeError("You need to log in to the seller central account in the Amazon instance.")
	def get_prod_info(self):
		return self.__prod_info
	def set_prod_info(self, x):
		self.__prod_info = x


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
		d_asin = self.__get_id_asin(p_id)
		if d_asin == 'Lookup':
			return False
		else:
			return True
	def create_asins(self):
		for i in __id_create_queue:
			cat_update_inst.prod_go_to(i)
			desc = Amzn_lst_single(cat_update_inst.descriptor_get())
			#adds barcode
			#############THIS WILL RETURN THE SAME BARCODE FOR EVERY SINGLE PRODUCT ID FIX THIS!!!###############
			desc["Barcode"] = self.dbObject.query("SELECT * from barcodes LIMIT 1;")[0][0]
			self.__prod_info.append(desc)
		for i in self.__prod_info:
			res = amazon_inst.add_single(i)
			#after successful add it deletes the barcode
			#need to add all of the exception handling in add_csv method 
			if res:
				self.dbObject.cust_com("DELETE from barcodes WHERE barcode = {0};".format(i["Barcode"]))




		

#need method that collects product information from catalog and makes an ASIN with it













