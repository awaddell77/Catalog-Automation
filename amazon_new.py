from soupclass8 import *
import time


class Asin_create(object):
	def __init__(self, p_list='', dir_n ="C:\\Users\\Owner\\Desktop\\I\\", *args):
		self.__dir_n = dir_n
		#self.p_list = conv_to_dict(p_list, self.dir_n)
		#self.dbObject = Db_mngmnt(text_cred[2],text_cred[3],'asins', '192.168.5.90')
		self.p_list = []
		self.args = args
		self.browser = ''
		#self.header = r_csv_2(p_list, mode = 'rb', encoding = 'ISO-8859-1' )[0]
		self.asins = []
		self.__fail_lst = []
		#self.merch_ids = text_l("C:\\Users\\Owner\\Documents\\Important\\amazon_creds.txt")
		self.merch_ids = ['000', '111']
		self.csv_dir = ''
		#if abort_delay is True add_single(x) method won't wait 30 seconds to return an error 
		self.abort_delay = False
	def set_dir(self, x):
		self.__dir_n = x
	def get_dir(self):
		return self.__dir_n

	def get_p_lst(self):
		return self.p_list
	def set_p_lst(self, x):
		self.p_lst = x
	def toggle_mkt(self, x):
		if x in ['magic', 'Magic', 'mtg', 'MTG']:
			command = """ 
				var magic_opt = '/merchant-picker/change-merchant?url=%2F&marketplaceId={0}&merchantId={1}"'
				for (i = 0 ; i < document.getElementById('sc-mkt-picker-switcher-select').children.length ; i++){
					if (document.getElementById('sc-mkt-picker-switcher-select').children[i].children[0] == magic_opt){
						document.getElementById('sc-mkt-picker-switcher-select').children[i].children[0].click()
					}
				}
				""".format(self.merch_ids[0], self.merch_ids[1])
			self.browser.js(command)
		#not finished
	def go_to_search_page(self):
		self.browser.go_to("https://sellercentral.amazon.com/inventory/")
		if self.load_check('inventory'):
			time.sleep(.5)




	def start(self):
		self.browser = Sel_session("https://sellercentral.amazon.com/gp/homepage.html")
		self.browser.start()
	def url(self):
		return self.browser.driver.current_url

	def get_asins(self):
		return self.asins
	def set_asins(self, x):
		self.asins = x

	def add_single(self, x ):
		start_time = time.time()
		n = 0
		self.browser.go_to("https://catalog.amazon.com/abis/Classify/SelectCategory?itemType=collectible-single-trading-cards&productType=TOYS_AND_GAMES")
		#name
		self.browser.js("document.getElementById('item_name').value = '{0}'".format(prep(x["Product Name"])))
		#manufacturer
		self.browser.js("document.getElementById('manufacturer').value = '{0}'".format(prep(x["Manufacturer"])))
		#brand name
		self.browser.js("document.getElementById('brand_name').value = '{0}'".format(prep(x["Manufacturer"])))
		#minimum age
		self.browser.js("document.getElementById('mfg_minimum').value = '{0}'".format(prep(x["Ages"])))
		#minimum age units
		self.browser.js("document.getElementById('mfg_minimum_unit_of_measure').value = '{0}'".format("years"))
		#barcode
		self.browser.js("document.getElementById('external_product_id').value = '{0}'".format(prep(x["Barcode"])))
		#barcode type
		self.browser.js("document.getElementById('external_product_id_type').value = '{0}'".format(prep(str(x["Barcode Type"]).lower())))
		#clicks over to Offer tab
		self.browser.js("document.getElementById('offer-tab').click()")
		time.sleep(1)
		#SKU
		self.browser.js("document.getElementById('item_sku').value = '{0}'".format(x["Product Id"]))
		#quantity
		self.browser.js("document.getElementById('quantity').value = '0'")
		#condition
		self.browser.js("document.getElementById('condition_type').value = 'collectible, like_new'")
		#MSRP
		self.browser.js("document.getElementById('standard_price').value = '{0}'".format(x["MSRP"]))
		#Quantity
		self.browser.js("document.getElementById('quantity').value = '0'")
		#switch over to image tab
		self.browser.js("document.getElementById('image-tab').click()")
		time.sleep(1)
		#Image
		self.add_image(x["Product Image"])
		time.sleep(5)
		#switch over to Description tab
		self.browser.js("document.getElementById('tang_description-tab').click()")
		time.sleep(1)
		#Add description
		self.browser.js("document.getElementById('product_description').value = '{0}'".format(prep(x["Description"])))
		#switch over to Keywords tab
		self.browser.js("document.getElementById('tang_keywords-tab').click()")
		time.sleep(1)
		#adds keyword
		self.browser.js("document.getElementById('target_audience_keywords1').value = '{0}'".format(prep(x["Keywords"])))
		time.sleep(.5)
		#clicks back on the vital info tab
		self.browser.js("document.getElementById('tang_vital_info-tab').click()")
		time.sleep(1)

		while not self.browser.is_enabled("main_submit_button"):
			n += 1
			time.sleep(.5)
			if n >= 20:
				raise Amazon_Validation_Error("Amazon will not validate {0}".format(x["Product Name"]))
		if self.browser.is_enabled("main_submit_button"):
			#this is for testing only
			self.browser.js("document.getElementById('main_submit_button').click()")
			print("CLICKED THE SUBMIT BUTTON!")
			load_check_abort = 0
			#has to wait for the page to transition to the seller central page
			print("Waiting for sellercentral page", end='')
			while self.load_check('sellercentral'):
				print(".", end='')
				load_check_abort += 1
				time.sleep(1)
				if load_check_abort > 30 and self.abort_delay:
					print()
					raise RuntimeError("Amazon either took too long to respond or objected to the item.")
			print()
			print("Found sellarcentral page. Process took {0} seconds.".format(time.time() - start_time))

			return True
		else:
			return False

	def add_image(self, x):
		if "http://" in x:
			x = fn_grab(x)
		x =  self.get_dir() + x

		self.browser.js("return document.getElementById('Parent-ProductImage_MAIN-div').children[2].getElementsByTagName('input')[10]").send_keys(x)
	def update_single(self, x ):
		#self.browser.go_to("https://catalog.amazon.com/abis/product/DisplayEditProduct?marketplaceID=ATVPDKIKX0DER&ref=xx_myiedit_cont_myifba&sku={0}&asin={1}".format(x["Product Id"], x['asin'], self.merch_ids[0]))
		#updates name
		self.browser.js("document.getElementById('item_name').value = '{0}'".format(prep(x["Product Name"])))
		#clicks over to image tab to update image
		self.browser.js("document.getElementById('image-tab').click()")
		time.sleep(1)
		#removes the image
		self.browser.js("document.getElementById('Parent-ProductImage_MAIN-div').children[2].getElementsByTagName('button')[0].click()")
		#adds new image
		self.add_image(x["Product Image"], self.get_dir())
		#updates description
		self.browser.js("document.getElementById('product_description').value = '{0}'".format(prep(x["Description"])))

		while not self.browser.is_enabled("main_submit_button"):
			n += 1
			time.sleep(.5)
			if n >= 30:
				raise Amazon_Validation_Error("Amazon will not validate {0}".format(x["Product Name"]))
		if self.browser.is_enabled("main_submit_button"):
			#this is for testing only
			self.browser.js("document.getElementById('main_submit_button').click()")
			print("CLICKED THE SUBMIT BUTTON!")
			load_check_abort = 0
			#has to wait for the page to transition to the seller central page
			while self.load_check('sellercentral'):
				print("Waiting for sellercentral page")
				load_check_abort += 1
				time.sleep(1)
				if load_check_abort > 30:
					raise RuntimeError("Amazon either took too long to respond or objected to the item.")
			print("Found sellarcentral page. Process took {0} seconds.".format(time.time() - start_time))

			return True
		else:
			return False
	def source(self):
		return self.browser.source()



	def add_csv(self):
		dir_n = self.csv_dir
		succ_list = [self.header]
		fail_list = [self.header]
		for i in range(0, len(self.p_list)):
			try:
				outcome = self.add_single(self.p_list[i], dir_n)
			except Amazon_Validation_Error as AVE: #untested
				print("Error occurred:")
				print(AVE)
				print("Trying again but with EAN")
				try:
					self.p_list[i]["Barcode Type"] = 'ean'
					outcome = self.add_single(self.p_list[i], dir_n)
				except Amazon_Validation_Error as AVE:
					self.p_list[i] = barcode_handling(self.p_list[i])
					fail_list.append(S_format(self.p_list[i]).d_sort(self.header))

				#self.p_list[i] = barcode_handling(self.p_list[i])
				#fail_list.append(S_format(self.p_list[i]).d_sort(self.header))
			except:
				#general
				self.p_list[i] = barcode_handling(self.p_list[i])
				print("General Error Occurred with {0}".format(self.p_list[i]["Product Name"]))
				fail_list.append(S_format(self.p_list[i]).d_sort(self.header))

			else:
				if outcome:
					succ_list.append(S_format(self.p_list[i]).d_sort(self.header))
				else:
					self.p_list[i] = barcode_handling(self.p_list[i])
					fail_list.append(S_format(self.p_list[i]).d_sort(self.header))

			time.sleep(1)
		w_csv(succ_list, "SUCCESS LIST.csv")
		w_csv(fail_list, "FAILED ADDS.csv")
	def retrieve_asins(self):
		for i in range(0, len(self.p_list)):

			self.asins.append(self.grab_asin(self.p_list[i]["Product Id"]))
		w_csv(self.asins, "ASIN_list.csv")
	def grab_asin(self, name1):
		wait = 3
		#retrieves ASIN that has already been created. Need product id.
		#name == Product Id or Item Sku on Amazon 
		#needs to be on the "Manage Inventory" page
		#name = re.sub("'", "39;", name) #used to be \\'
		try:
			int(name1)
		except ValueError as VE:
			name1 = re.sub("'", rep, name1)
			if "Foil" not in name:
				name_1 = name1 + " NOT Foil"
			else:
				name_1 = name1
		else:
			name_1 = str(name1)

		self.browser.js("document.getElementById('myitable-search').value ='" + name_1 + "' ;")
		self.browser.js("document.getElementById('myitable-search-button').children[0].children[0].click();")
		time.sleep(wait)
		site = self.browser.source()
		name = name1
		#ASIN = self.browser.js("return document.getElementById('NjIzMjk2Mw_e_e-title-asin').children[0].children[0].innerHTML;")
		try:
			ASIN = re.sub('\n', '', site.find('div', {'data-column':'asin'}).text).strip()
			name = re.sub('\n', '', site.find('div', {'data-column':'sku'}).text).strip()
		except TypeError as TE:
			return [name, "None"]
		except AttributeError as AE:
			return [name, "None"]
		else:
			return [name, ASIN]



	def load_check(self, start):
		#checks to see if self.browser has switched to the sellercentral page after clicking on the save button on the item creation page
		if self.browser.js('return document.readyState') != "complete" or start not in self.browser.driver.current_url:
			return True
		else:
			return False
def barcode_handling(x):
	d = x 
	d["Barcode"] = '[' + str(d["Barcode"])
	return d


class Crit_not_present(Exception):
	pass
class Value_not_appr(Exception):
	#for when the contents are not appropriate or valid
	pass
class Image_not_found(Exception):
	#for when it cannot find the images
	pass
class Amazon_Validation_Error(Exception):
	pass
def prep(x):
	value = x
	value = re.sub("'", "\\\'",  value)
	value = re.sub('"', '\\\"', value)
	return value
def conv_to_dict(x, dir_n = "C:\\Users\\Owner\\Desktop\\I\\"):
	#can accept either a list of dicts or a csv file name
	if type(x) == list:
		for i in range(0, len(x)):
			if type(x[i]) != dict:
				raise TypeError("Item #{0} is not a dictionary.".format(str(i)))
		new_x = x[:]
	else:
		new_x = dictionarify(x)
	crits = ['Manufacturer', 'Product Image', 'Barcode Type', 'Barcode', 'Product Id', 'MSRP', 'Product Name', 'Description', 'Ages', 'Keywords']
	for i_2 in range(0, len(new_x)):
		#checks to see if Image Link is present if Product Image field is not, then creates a product image field by extracting the file name from the url
		if "Product Image" not in list(new_x[i_2].keys()) and "Image Link" in list(new_x[i_2].keys()):
			new_x[i_2]["Product Image"] = fn_grab(new_x[i_2]["Image Link"])
		for i in range(0, len(crits)):
			#checks each dict to see if they have the necessary fields
			req_field_pres = crits[i] not in list(new_x[i_2].keys())
			missing_crit = ke_check(new_x[i_2], crits[i])
			empty_field = empty_check(new_x[i_2], crits[i])
			if req_field_pres or missing_crit or empty_field:
				if req_field_pres:
					raise Crit_not_present("CSV is missing a required field: {0}".format(crits[i]))
				if missing_crit:
					raise Crit_not_present("Item #{0} is missing a required field: {1}".format(str(i_2), crits[i]))
				if empty_field:
					raise Crit_not_present("The {0} field in item #{1} was left blank.".format(crits[i], str(i_2)))
		#checks to see if fields contain appropriate content (i.e. the correct type of data)
		b_code_er, p_id_er, msrp_er = number_check(new_x[i_2]["Barcode"]), number_check(new_x[i_2]["Product Id"]), number_check(new_x[i_2]["MSRP"])
		if b_code_er or p_id_er or msrp_er:
			if b_code_er:
				raise Value_not_appr("Barcode value {0} for Item #{1} (Product Name: {2}) is invalid".format(new_x[i_2]["Barcode"], str(i_2), new_x[i_2]["Product Name"]))
			if p_id_er:
				raise Value_not_appr("Product Id {0} for Item #{1} (Product Name: {2}) is invalid".format(new_x[i_2]["Product Id"], str(i_2), new_x[i_2]["Product Name"]))
			if msrp_er:
				raise Value_not_appr("MSRP {0} for Item #{1} (Product Name: {2}) is invalid".format(new_x[i_2]["MSRP"], str(i_2), new_x[i_2]["Product Name"]))
		if not image_check(new_x[i_2]["Product Image"], dir_n):
			raise Image_not_found("Image file {0} not found in directory {1}".format(new_x[i_2]["Product Image"], dir_n))
	return new_x





	#would check if the criteria were there and also if they were valid
def ke_check(x, key):
	#returns true for key errors
	try:
		x[key]
	except KeyError as KE:
		return True
	else:
		return False
def empty_check(x, key):
	#returns true if value is empty of '' AND ONLY when that is the case. If there is no such key it returns false anyways
	try:
		contents = x[key]
	except KeyError as KE:
		return False
	else:
		if contents == '':
			return True
		else:
			return False

def number_check(x):
	#checks to see if barcode, product Id, MSRP are numbers. Returns True if error is detected
	try:
		int(x)
	except ValueError as VE:
		try:
			float(x)
		except ValueError as VE:
			return True
		else:
			return False
def image_check(x, dir_n = "C:\\Users\\Owner\\Desktop\\I\\"):
	full_path = dir_n + x
	if os.path.exists(full_path):
		return True
	if not os.path.exists(full_path):
		return False

def run_prog(x):
	x = ''
	accept = ["Yes", 'y', 'Y']
	exit = ["Exit", "q", "Q", 'bye', 'N', 'n']
	while x not in accept or exit:
		x = input("Proceed with program (Y/N)?: ")
		if x == "END":
			break
	if x in accept:
		return True
	else:
		return False





#test_inst = Main('test_adds.csv')

if __name__ == "__main__":
	if sys.argv[1] == '-h':
		print("python3 [prog_name.py] \"[csv file name]\" [-nd] [Full path to new directory for images]")
	else:
		m_inst = Asin_Add_Main(sys.argv[1])
		res = run_prog(1)
		if res and sys.argv[2] == '-nd':
			m_inst.add_csv(sys.argv[3])
		elif res:
			m_inst.add_csv()
		else:
			self.browser.close()
