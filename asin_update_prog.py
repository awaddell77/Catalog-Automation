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
		#product ids that need to get product information
		self.__id_create_queue = []
		#for product Ids coupled with asins
		self.__asin_id_lst = []
		#used for start_up_all method
		self.__amazon_online = False
		#for successful ASIN creates
		self.__fail_lst = []
		#for items that have ASINs that need to be retrieved during the ASIN creation process 
		self.__retr_lst = []
		#
		self.__keep_live_check = time.time()
		self.asin_create_timer = 0
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
	def get_asin_id_lst(self):
		return self.__asin_id_lst
	def set_asin_id_lst(self, x):
		self.__asin_id_lst = x


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
		p_ids = self.dbObject.query("SELECT * FROM {0};".format(str(table_name)))
		p_ids = [i[0] for i in p_idges]
		self.set_id_queue(p_ids)
	def move_ids(self):
		#assings value of id_queue to id_create_queue, then removes all of the product ids from id_to_check table on database
		#deletes ids from database
		p_ids = self.get_id_queue()
		self.set_id_create_queue(p_ids)

		for i in p_ids:
			self.dbObject.cust_com("DELETE FROM id_to_check WHERE product_id = \"{0}\";".format(str(i)))
	def remove_ids(self):
		for i in __id_check_queue:
			pass
	def get_fail_lst(self):
		return self.__fail_lst
	def set_fail_lst(self, x):
		self.__fail_lst = x

	def get_retr_lst(self):
		return self.__retr_lst
	def set_retr_lst(self, x):
		self.__retr_lst = x
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
	def cat_get_asins(self, x):
		#retrieves individual asins from catalog, returns a list
		results = []
		for i in x:
			results.append(self.__get_id_asin(i))
		return results

	def __grab_barcodes(self, num):
		barcodes = self.dbObject.query("SELECT * from barcodes LIMIT {0};".format(num))
		if len(barcodes) < num:
			raise RuntimeError("Only found {0} barcodes.".format(len(barcodes)))
		return barcodes
	def bcode_test(self, num):
		#remove after testing
		return self.__grab_barcodes(num)
	def import_csv(self, x):
		prod_ids = dictionarify(x)
		return [i["Product Id"] for i in prod_ids]

	def get_descriptions(self):
		barcodes_lst = self.__grab_barcodes(len(self.__id_create_queue))
		self.set_barcode_queue([i[0] for i in barcodes_lst])
		bcodes = self.get_barcode_queue()
		p_ids = self.get_id_create_queue()
		for i in range(0, len(p_ids)):
			self.cat_update_inst.prod_go_to(p_ids[i])
			desc = Amzn_lst_single(self.cat_update_inst.descriptor_get()).form()
			desc["Barcode"] = bcodes[i]
			self.__prod_info.append(desc)
		return self.get_prod_info()

	def create_asins(self):
		#self.asin_create_timer = time.time()
		count = 1
		for i in self.__prod_info:
			print("Attempting {0}. #{1} of {2}".format(i["Product Name"],count, len(self.__prod_info)))
			try:
				res = self.amazon_inst.add_single(i)
			except Amazon_Validation_Error as AVE: #untested
				print("Error occurred:")
				print(AVE)
				print("Trying again but with EAN")
				try:
					i["Barcode Type"] = self.switch_bcode_type(i["Barcode Type"])
					res = self.amazon_inst.add_single(i)
				except Amazon_Validation_Error as AVE:
					self.__fail_lst.append(i)
			except KeyboardInterrupt as KI:
				break

			except:
				#general

				print("General Error Occurred with {0}".format(i["Product Name"]))
				print(sys.exc_info()[:])
				self.__fail_lst.append(i)
				count += 1

			else:
				if res:
					self.__retr_lst.append(i)
					count += 1
				else:
					self.__fail_lst.append(i)
					count += 1
		#duration = time.time() - self.asin_create_timer()
		#print("Process took {0} seconds to complete.".format(duration))
		print("{0} ASINs were created. Failed to create: {1}".format(len(self.__retr_lst), len(self.__fail_lst)))
	def m_process(self):
		#creates asins then retrieves them
		print("Retrieving product information from catalog.")
		self.get_descriptions()
		print("Creating ASINs")
		self.create_asins()
		print("Obtaining ASINs from Amazon")
		self.get_asins()
		print("Fetched ASINs. Now updating product ASINs in catalog")
		self.update_asins()
		print("Updated product ASINs in catalog. Now deleting used barcodes from database.")
		self.delete_bcodes()
		self.set_prod_info([])

	def switch_bcode_type(self, x):
		if x == 'ean':
			return 'upc'
		elif x == 'upc':
			return 'ean'
	def delete_bcodes(self):
		succ_lst = self.get_retr_lst()
		for i in succ_lst:
			self.dbObject.cust_com("DELETE from barcodes WHERE barcode = \"{0}\";".format(i["Barcode"]))
	def get_asins(self):
		p_ids = self.get_retr_lst()
		for i in p_ids:
			self.__asin_id_lst.append(self.amazon_inst.grab_asin(i["Product Id"]))
	def update_asins(self):
		for i in self.__asin_id_lst:
			self.cat_update_inst.go_to(i[0])
			if i[1] != "None":
				#not pythonic but the only way to ensure it doesn't add string containing "None"
				#also ASINs aren't always alphanumeric and can contain only letters
				self.cat_update_inst.update_descriptor_all('Asin', i[1])
				self.cat_update_inst.click_update()
				self.cat_update_inst.load_check()
	def keep_live(self, interval = 30):
		diff = time.time() - self.__keep_live_check
		if diff > interval:
			self.amazon_inst.browser.go_to("https://sellercentral.amazon.com/gp/homepage.html")
			self.__keep_live_check = time.time()








def export_csv13(lst):
	results = []
	headers = list(lst[0].keys())
	#results = results + headers

	for i in lst:
		results.append(S_format(i).d_sort(headers))
	w_csv(results, "exported_lst.csv")
	return results




		

#need method that collects product information from catalog and makes an ASIN with it













