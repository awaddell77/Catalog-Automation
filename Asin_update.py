#auto-update
from Cat_session import *
from Cat_update import *
from amazon_new import *
from Amazon_list_format import *
from Cat_dbase import *
from text_l import *
import time

class Asin_update:
	def __init__(self, host ='192.168.5.90', credFile = 'C:\\Users\\Owner\\Documents\\Important\\catcred.txt',
		credfile2 = 'C:\\Users\\Owner\\Documents\\Important\\cat_cred2.txt',*args):
		#database connection
		self.text_cred = text_l(credFile)
		self.dbObject = Db_mngmnt(self.text_cred[2], self.text_cred[3],'asins', host)
		#catalog database connection
		#TODO add way to use different credentials using arguments in Cat_dbase and Asin_update
		self.cat_obj = Cat_dbase()
		#makes object return the product information dicts with the proper key names
		self.cat_obj.set_proper_desc(True)
		#catalog update instance
		self.cat_update_inst = Cat_update(credFile2)
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
		self.retryCreate = True
		self.attemptDelay = False
	def start_up_all(self):
		#self.cat_update_inst.start()
		self.amazon_inst.start()
		'''amazon_counter = time.time()
		while not self.__amazon_online:
			if self.amazon_inst.url() in ["https://sellercentral.amazon.com/gp/homepage.html?", "https://sellercentral.amazon.com/gp/homepage.html/ref=ag_home_logo_xx"]:
				self.__amazon_online = True
				break
			elif (time.time() - amazon_counter) >= 30:
				raise RuntimeError("You need to log in to the seller central account in the Amazon instance.")'''
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
	def get_ids_cat(self, cat_id, asin_filter = True):
		#takes ids from catalog
		#used for updating specific categories
		#by default it only returns those products that don't have ASINs
		if asin_filter:
			p_ids = self.cat_obj.cat_need_asin(cat_id)
			self.set_id_queue(p_ids)
		else:
			p_ids = self.cat_obj.get_category_contents(cat_id, True)
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
	def barcode_dump(self, num):
		bcodes = self.__grab_barcodes(num)

	def import_csv(self, x):
		prod_ids = dictionarify(x)
		return [i["Product Id"] for i in prod_ids]

	def get_descriptions(self, get_images = True):
		self.set_prod_info([])
		barcodes_lst = self.__grab_barcodes(len(self.__id_create_queue))
		self.set_barcode_queue([i[0] for i in barcodes_lst])
		bcodes = self.get_barcode_queue()
		p_ids = self.get_id_create_queue()
		for i in range(0, len(p_ids)):
			#self.cat_update_inst.prod_go_to(p_ids[i])
			prod_info = self.cat_obj.get_product(p_ids[i])
			desc = Amzn_lst_single(prod_info)
			desc.set_d_opt(get_images)
			desc = desc.form()
			#desc = Amzn_lst_single(self.cat_update_inst.descriptor_get()).form()
			desc["Barcode"] = bcodes[i]
			self.__prod_info.append(desc)
		return self.get_prod_info()

	def create_asins_v2(self, limit = 10):
		#should keep on trying to add the single item
		self.__retr_lst = []
		self.__fail_lst = []
		start = time.time()
		count = 1
		n_limit = 0
		kI = False

		for i in self.__prod_info:

			while True and not kI:
				if self.attemptDelay: time.sleep(30)
				if n_limit > limit:
					print("Retried {0} times with no success".format(limit))
					n_limit = 0
					count += 1
					break
				try:
					print("Attempting {0}. #{1} of {2}".format(i["Product Name"],count, len(self.__prod_info)))
				except UnicodeEncodeError as UE:
					print("UnicodeEncodeError on #{0} of {1}. Proceeding with ASIN creation".format(count, len(self.__prod_info)))

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
						#count += 1
						n_limit += 1



					except:
						print("General Error Occurred with {0}".format(i["Product Name"]))
						print(sys.exc_info()[:])
						self.__fail_lst.append(i)
						#count += 1
						n_limit += 1
						#break

				except RuntimeError as RE:
					#while not res and n_limit < limit:
					if self.AmazonUnavailable():
						#res = self.amazon_inst.add_single(i)
						n_limit += 1


				except KeyboardInterrupt as KI:
					kI = True
					break

				except:
					#general

					print("General Error Occurred with {0}".format(i["Product Name"]))
					print(sys.exc_info()[:])
					self.__fail_lst.append(i)
					count += 1
					break

				else:
					if res:
						self.__retr_lst.append(i)
						count += 1
						break
					else:
						self.__fail_lst.append(i)
						count += 1

		#duration = time.time() - self.asin_create_timer()
		#print("Process took {0} seconds to complete.".format(duration))
		end = time.time()
		duration = end - start
		print("{0} ASINs were created. Failed to create: {1}".format(len(self.__retr_lst), len(self.__fail_lst)))
		print("ASIN creation process took {0} seconds".format(duration))

	def create_asins(self):
		self.__retr_lst = []
		self.__fail_lst = []
		start = time.time()
		count = 1
		for i in self.__prod_info:
			try:
				print("Attempting {0}. #{1} of {2}".format(i["Product Name"],count, len(self.__prod_info)))
			except UnicodeEncodeError as UE:
				print("UnicodeEncodeError on #{0} of {1}. Proceeding with ASIN creation".format(count, len(self.__prod_info)))

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
					count += 1
				except:
					print("General Error Occurred with {0}".format(i["Product Name"]))
					print(sys.exc_info()[:])
					self.__fail_lst.append(i)
					count += 1
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
		end = time.time()
		duration = end - start
		print("{0} ASINs were created. Failed to create: {1}".format(len(self.__retr_lst), len(self.__fail_lst)))
		print("ASIN creation process took {0} seconds".format(duration))
	def asin_create_m_cats(self, cats):
		p_ids = []
		self.cat_obj.reconnect()
		self.dbObject.reconnect()
		if not isinstance(cats, list):
			raise TypeError("Param must be list")
		for i in cats:
			#gets every product id in the category that does not have an ASIN
			self.get_ids_cat(str(i))
			p_ids += self.get_id_queue()
		self.set_id_create_queue(p_ids)
		#creates the proper dicts for amazon submission
		self.get_descriptions()
		#creates the asins
		if self.retryCreate:
			#calls method that tries to create amazon listing several more times if it errors out the first time
			self.create_asins_v2()
		else:
			self.create_asins()
		self.amazon_inst.go_to_search_page()

		#retrieves and then updates the ASIN descriptors in the catalog
		#also deletes the barcodes that were used from the barcode table in the database
		self.get_asins()


	def m_process(self):
		#creates asins then retrieves them
		print("Retrieving product information from catalog.")
		self.get_descriptions()
		print("Creating ASINs")
		self.create_asins()
		print("Obtaining ASINs from Amazon")
		self.amazon_inst.go_to_search_page()
		self.get_asins()
		print("Fetched ASINs. Now updating product ASINs in catalog")
		self.update_asins()
		print("Updated product ASINs in catalog. Now deleting used barcodes from database.")
		self.delete_bcodes()
		self.set_prod_info([])
	def c_g_asins(self):
		#creates and then updates ASINs
		self.create_asins()
		self.amazon_inst.go_to_search_page()
		self.get_asins()
		self.update_asins()

	def switch_bcode_type(self, x):
		if x == 'ean':
			return 'upc'
		elif x == 'upc':
			return 'ean'
	def delete_bcodes(self):
		succ_lst = self.get_retr_lst()
		print("Deleting barcodes")
		self.dbObject.reconnect()#not the best solution, definitely need to have a try/except block for lost connections instead
		for i in succ_lst:
			self.dbObject.cust_com("DELETE from barcodes WHERE barcode = \"{0}\";".format(i["Barcode"]))
		self.set_barcode_queue([])
	def delete_bcodes_n(self, n):
		print("Deleting barcodes")
		barcodes = self.dbObject.query("SELECT * from barcodes LIMIT {0};".format(n))
		succ_lst = [i[0] for i in barcodes]
		self.dbObject.reconnect()#not the best solution, definitely need to have a try/except block for lost connections instead
		for i in succ_lst:
			print("DELETING {0}".format(str(i)))
			self.dbObject.cust_com("DELETE from barcodes WHERE barcode = \"{0}\";".format(i))

	def get_asins(self, update_all = False, update = True):
		#if update argument is true then the method automatically updates the products in the catalog with their new ASINs
		self.__asin_id_lst = []
		self.amazon_inst.go_to_search_page()
		#if update_all is true then it searches for ASINs using all of the product ids, even if they aren't on the retr_lst
		if update_all:
			p_ids = self.get_id_create_queue()
			p_ids = [{"Product Id": str(i)} for i in p_ids]
		else:
			p_ids = self.get_retr_lst()
		for i in p_ids:
			self.__asin_id_lst.append(self.amazon_inst.grab_asin(i["Product Id"]))
		if update:
			self.update_asins()
			self.delete_bcodes()
	def update_asins(self, sql = True):
		issues = []
		self.cat_obj.reconnect()
		for i in range(0, len(self.__asin_id_lst)):
			#not pythonic but the only way to ensure it doesn't add string containing "None"
			#also ASINs aren't always alphanumeric and can contain only letters

			if self.__asin_id_lst[i][1] != "None":
				if sql:
					try:
						self.cat_obj.update_product(str(self.__asin_id_lst[i][0]), 'asin', self.__asin_id_lst[i][1])
					except KeyboardInterrupt as KE:
						break
					except:
						print("General error occured")
						print(sys.exc_info()[:])
						issues.append(str(self.__asin_id_lst[i][0]))


				else:
					self.cat_update_inst.go_to(i[0])
					self.cat_update_inst.update_descriptor_all('Asin', i[1])
					self.cat_update_inst.click_update()
					self.cat_update_inst.load_check()
		if not issues:
			print("Ran into issues updating the following products")
			return issues
	def retr_asins_for_cat(self, cat_id, asin_filter = True):
		#retrieves product ids from catalog, puts them into a list of dictionaries and then assigns that list to retr_lst
		self.get_ids_cat(cat_id, asin_filter)
		p_ids = self.get_id_queue()
		results = [{"Product Id": str(i)} for i in p_ids]

		self.set_retr_lst(results)
		self.get_asins()


	def keep_live(self, interval = 30):
		diff = time.time() - self.__keep_live_check
		if diff > interval:
			self.amazon_inst.browser.go_to("https://sellercentral.amazon.com/gp/homepage.html")
			self.__keep_live_check = time.time()
	def wait_stay_live(self, interval = 30):
		while True:

			try:
				time.sleep(30)

			except KeyboardInterrupt as KE:
				break
			else:
				self.amazon_inst.browser.go_to("https://sellercentral.amazon.com/gp/homepage.html")
	def AmazonUnavailable(self):
		site = self.amazon_inst.source()
		title = site.find("head").find('title')
		if title is None:
			return False
		elif title.text == 'Website Temporarily Unavailable':
			return True
		else:
			return False
	def updateTest(self, p_id):
		#static method for testing amazon update function
		prod_info = self.cat_obj.get_product(p_ids)
		self.amazon_inst.update_single(prod_info)














def export_csv13(lst):
	results = []
	headers = list(lst[0].keys())
	#results = results + headers

	for i in lst:
		results.append(S_format(i).d_sort(headers))
	w_csv(results, "exported_lst.csv")
	return results






#need method that collects product information from catalog and makes an ASIN with it
