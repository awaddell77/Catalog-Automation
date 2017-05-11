from soupclass8 import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import getpass
import sys, re
import time
from log import entry_maker
from dbaseObject import *
from Imprt_csv import *
from Cat_dbase import *
from d_copy import *

text_cred = text_l('C:\\Users\\Owner\\Documents\\Important\\catcred.txt')
class Cat_session(object):#parent class for this pseudo-API
	def __init__(self, *args):
		#self.username = input('Username:') 
		#self.password = getpass.getpass('Password:')
		self.username = text_cred[0]
		self.password = text_cred[1]
		self.driver = ''
		self.dbObject = Db_mngmnt(text_cred[2],text_cred[3],'preorders', '192.168.5.90')
		self.cat_dbase = Cat_dbase()
		#in the future allow the user to select which browser to use (would need to make this a child of a parent that did that)
		#self.driver = webdriver.PhantomJS()
		self.args = args
		self.__del_items = []
	def start_browser(self):
		self.driver = webdriver.Firefox()
	def get_del_items(self):
		return self.__del_items
	def set_del_items(self, x):
		self.__del_items = x
	def main(self):
		terminate = ['Log off','Logout', 'Exit']
		self.session_start()
		data = ''
		#return self.driver
		while data not in terminate:
			data = input('>>')
			self.interpreter(data)

	def source(self):
		return bs(self.driver.page_source, 'lxml')


	def interpreter(self,*args):
		print('This is the command: %s' % (args))
		'''if 'Search' in args:
			x = args.split('')
			return self.prod_s(x[1])'''
	def url(self):
		return self.driver.current_url


	def start(self):#login method
		if not self.driver:
			#starts browser if it isn't already open
			self.start_browser()

		self.driver.get('https://accounts.crystalcommerce.com/users/sign_in')
		element = self.driver.find_element_by_id('user_email')
		element1 = self.driver.find_element_by_id('user_password')
		element.send_keys(self.username)
		element1.send_keys(self.password)
		element3 = self.driver.find_element_by_name('commit')# sign in button
		element3.click()
		self.target()
		while self.driver.current_url == 'https://catalog.crystalcommerce.com/users/login':
			time.sleep(.5)
		return self.driver
	def target(self):
		element = self.driver.find_element_by_link_text('Catalog')
		element.click()
		if self.driver.current_url == 'https://catalog.crystalcommerce.com/users/login':#checks to see if it got kicked back
			element_1 = self.driver.find_element_by_class_name('sinewave-button')
			element_1.click()

		else:
			return self.driver
	def cat_grab(self):#untested
		#grabs all the current categories
		self.driver.get('https://catalog.crystalcommerce.com/categories')
		element_1 = self.driver.find_element_by_link_text('New Category')
		element_1.click()
		return self.driver
	def s_to_a(self,x):
		#navigates to item by using its product Id (x) and clicks the "Submit to Amazon" button
		self.prod_go_to(x)
		self.driver.execute_script(
			'''
			var f = document.getElementsByClassName('form-actions')[1];
			for (i = 0 ; i < f.children.length ; i++){
			if (f.children[i].innerHTML == "Submit to Amazon"){
      			f.children[i].click();
			}
			else{
    			console.log("DID NOT FIND IT");
			}}'''
			)
		while self.driver.execute_script('document.readyState') != 'complete':
			time.sleep(.5)
	def s_to_a_batch(self, x):
		p_ids = r_csv(x)
		#csv with just the product IDs
		for i in range(0, len(p_ids)):
			self.s_to_a(p_ids[i])
		return "Complete"

	def push_skus(self,x):
		self.cat_goto(x)
		try:
			checkbox = self.driver.find_element_by_id('all_products')
			#all_in_checkbox = self.driver.execute_script('return document.getElementById("product_variation_category_id").click()')
			checkbox.click()
			self.driver.execute_script('document.getElementById("product_variation_category_id").click()')
		except:
			print("Something went wrong")
			#self.driver.execute_script('document.getElementById("product_variation_category_id").click()')
		self.b_grab('btn btn-info','value', 'Push Skus to Clients').click()

	def push_asins(self,x):
		self.cat_goto(x)
		try:
			self.driver.execute_script("document.getElementById('all_products').click();")
			while self.driver.execute_script("return document.getElementById('all_products_in_category').style.display") == "none":
				time.sleep(.5)
			self.driver.execute_script('document.getElementById("product_variation_category_id").click()')
		except:
			print("Something went wrong.")
		self.b_grab('btn btn-info', 'value', 'Push ASINs to Clients').click()

	def push_asins_cc(self, x):
		#pushes ASINs for all child categories underneath a specified parent category (x)
		self.cat_goto(x)
		children = self.child_cats()
		for i in range(0, len(children)):
			self.push_asins(children[i])

	def push_skus_cc(self, x):
		#pushes skus for all child categories underneath a specified parent category (x)
		self.cat_goto(x)
		children = self.child_cats()
		for i in range(0, len(children)):
			self.push_skus(children[i])

	def push_pinfo_cc(self, x):
		#pushes product data  for all child categories underneath a specified parent category (x)
		self.cat_goto(x)
		children = self.child_cats()
		for i in range(0, len(children)):
			self.push_pinfo(children[i])

	def push_pinfo(self,x):
		self.cat_goto(x)
		try:
			checkbox = self.driver.find_element_by_id('all_products')
			#all_in_checkbox = self.driver.execute_script('return document.getElementById("product_variation_category_id").click()')
			checkbox.click()
			self.driver.execute_script('document.getElementById("product_variation_category_id").click()')
		except:
			print("Something went wrong")
			#self.driver.execute_script('document.getElementById("product_variation_category_id").click()')
		self.b_grab('btn btn-info','value', 'Push Product Data to Clients').click()

	def move_cat(self, x, target_cat):
		#moves a single item to a different category
		self.prod_go_to(x + '/edit')
		categories = self.driver.execute_script('document.getElementsByClassName("select required select2 wide-category-select")[0].children')
		#clicks on the drop down menu
		self.driver.execute_script('document.getElementsByClassName("select2-offscreen select2-focusser")[0].click();')
		#once the menu has been clicked the options are now visible 



	def prod_go_to(self, x):
		try:
			int(x)
		except ValueError as VE:
			return "{0} must be an integer".format(x)


		url = 'https://catalog.crystalcommerce.com/products/' + str(x)
		self.driver.get(url)


	def cat_find(self, x):
		categories = self.driver.execute_script('return document.getElementsByClassName("select required select2 wide-category-select")[0].children')
		for i in range(0, len(categories)):
			cat = categories[i].get_attribute('value')
			if x == cat:
				name = self.driver.execute_script('return document.getElementsByClassName("select required select2 wide-category-select")[0].children[%s].innerHTML;' % str(i))
				return name
		return
	def delete_product_single (self, x):
		self.prod_go_to(x)
		start = self.driver.current_url
		#ideally this function would store a temporary copy of the item in order to aid in
		#the recovery of items that were deleted by mistake
		self.driver.execute_script('''
			var items = document.getElementsByClassName('btn btn-danger');
			for (i = 0 ; i < items.length ; i++){
				if (items[i].innerHTML.contains('Delete')){
					items[i].click();
				}
			}


			''')
		try:
			self.driver.switch_to_alert().accept()
		except:
			return (x, False)
		while self.driver.execute_script('return document.readyState') != "complete" and self.driver.current_url == start:
			time.sleep(.5)
		print("Successfully deleted {0}".format(x))
		return x




	def descriptor_get(self, p_id=''):
		#returns the every descriptor on the product page as a dictionary
		#takes beautifulsoup object
		d = {}
		if p_id == '':
			d["Product Id"] = fn_grab(str(self.driver.current_url))
		else:
			d["Product Id"] = p_id
		bsObject = self.source()
		pi_page = bsObject.find('div', {'class':'product'})
		#default descriptors
		d["Product Name"] = pi_page.find('h2', {'class':'product_name'}).text
		d["Product Type"] = pi_page.find('h4', {'class': 'product_type_name'}).a.text
		#finding the image
		image_col = bsObject.find('div', {'class':'span4'})
		image_rows = image_col.find_all('li')
		image_link_element = image_rows[0].find('a',{'class':'thumbnail'})
		image_link = 'https:' + S_format(str(image_link_element)).linkf('href=').split('?')[0]
		d["Product Image Link"] = image_link
		d["Product Image"] = fn_grab(image_link) 
		table = pi_page.find('table')
		rows = table.find_all('tr')
		for i in range(0, len(rows)):
			value = rows[i].find('th').find_next('td').text
			value = value.replace('\n','')
			d[rows[i].find('th').text] = value
		d["Category Id"] = fn_grab(d.get("Category", "N/A"))
		#unique descriptors (i.e. the descriptors of the product type)
		desc_table = pi_page.find('table', {'id':'product_descriptors'}).tbody
		desc_rows = desc_table.find_all('tr')
		for i in range(0, len(desc_rows)):
			val = desc_rows[i].find('th').find_next('td').text
			d[desc_rows[i].find('th').text] = val.strip(' ')
		return d

	def quit(self):
		#quits the driver
		self.driver.quit()
	def refresh(self):
		self.driver.refresh()


	def b_grab(self, t_class, attribute, value): 
		#allows you to select a specific button given its class, attribute and that attribute's value
		items = self.driver.execute_script('return document.getElementsByClassName(%s)' % ('"' + t_class + '"'))
		if items == []:
			return "None found"
		for i in range(0, len(items)):
			r_value = items[i].get_attribute(attribute)
			if r_value == value:
				return items[i]
		return

	def child_cats(self):
		site = self.source()
		target = site.find('h3').find_next()
		links_r = S_table(target).table_eater_exp('a',1,3)
		new = [fn_grab(S_format(str(links_r[i])).linkf('<a href=')) for i in range(0, len(links_r))]
		return new










	def cat_goto(self, cat_number):
		self.driver.get('https://catalog.crystalcommerce.com/categories/' + cat_number) #goes to the category
		return self.driver
	def prod_s_cat(self,prod_name):#search within a given category once the driver is "parked" in the category
		element_1 = self.driver.find_element_by_id('product_search_name_cont')
		element_1.send_keys(prod_name)#puts product name in the search field
		element_1.send_keys(Keys.RETURN)




	def cat_s(self, cat_name):#searches for a category (cat_name)
		element_1 = self.driver.find_element_by_link_text('Categories')#
		element_1.click()
		element_2 = self.driver.find_element_by_id('categories_search_q')
		element_2.send_keys(cat_name)#puts cat_name into the search box
		element_2.send_keys(Keys.RETURN)#using keystroke key in order to avoid accidently clicking other buttons (in case they change in the future)
		return self.driver
	def prod_s(self, prod_name):
		element_1 = self.driver.find_element_by_name('q[name_cont]')
		element_1.send_keys(prod_name)
		element_1.send_keys(Keys.RETURN)
		return self.driver
	def prod_s_ADV(self, prod_name, *args):#advanced search feature, will be improved in the future
		pass

class S_results(object):#should probably be made a child of Cat_session once it is completed
	def __init__(self, site):#takes a webdriver object as site, calls its page_source method and then parses it through bs
		self.site = site.source() #turns the source into bsObject
		self.bsObject = bs(self.site, 'lxml') 


	def table_results_s(self):#returns the results on a singles results page in the catalog
		table = self.bsObject.find('table', {'class': 'table table-striped'})
		rows = table.find_all('tr', {'class':'product'})
		return rows #
	def cat_grab(self):#untested
		cats_cont = self.bsObject.find('select',{'id':'category_parent_id'})
		cats = cats_cont.find_all('option')
		new = [(S_format(str(cats[i])).linkf('<option value='), cats[i].text) for i in range(0, len(cats))]
		#new should be a list of tuples containin the category ID and the category name
		return new




class Cat_product_add(Cat_session):
	def __init__(self):
		super().__init__()
		#self.session = self.driver #didn't want to find and replace all the "session" references in the class
		self.__add_list = []
		self.__fail_lst = []
		#tba_lst and tba_fail_lst are for database adds
		self.__tba_lst = []
		self.__tba_fail_lst =[]
		self.__duplicates = []
		self.__dupe_check = False
		self.fname = ''
	def get_addlst(self):
		return self.__add_list
	def reset_addlst(self):
		self.__add_list = []

	def set_tba_list(self, x):
		if type(x) == str:
			self.__tba_lst = dictionarify(x)
		elif type(x) == list or type(x) == tuple:
			self.__tba_lst = x
		else:
			raise TypeError("Argument must be either filename (string), a tuple, or a list.")
	def get_tba_fail_lst(self):
		return self.__tba_fail_lst
	def set_tba_fail_lst(self, x):
		self.__tba_fail_lst = x
	def get_tba_list(self):
		return self.__tba_lst
	def get_fail_list(self):
		return self.__fail_lst
	def set_fail_list(self, x):
		if type(x) == str and '.' in x:
			self.__fail_lst = dictionarify(x)
		elif type(x) == lst or type(x) == tuple:
			self.__fail_lst = x
		else:
			raise TypeError("Argument must be either filename (string), a tuple, or a list.")
	def get_duplicates(self):
		return self.__duplicates
	def set_duplicates(self, x):
		self.__duplicates = x
	def get_dupe_check(self):
		return self.__dupe_check
	def set_dupe_check(self, x):
		self.__dupe_check = x



	def submit_addlst(self, data, columns, dbase, table):
		#data argument = keys which hold the desired values
		items = self.get_addlst()
		for i in items:
			data_fields = []
			for i_2 in data: #take out of loop if speed becomes an issue 
				data_fields.append[i[i_2]]
			try:
				self.dbase_add(data_fields, columns, dbase, table)
			except:
				print("{0} was not added to the database.".format(i["Product Name"]))
			else:
				print("{0} was added to table \"{1}\" in databse \"{2}\" ".format(i["Product Name"], table, dbase))
	def submit_tbalst(self, data, columns, dbase, table):
		#data argument = keys which hold the desired values
		items = self.get_tba_list()
		for i in items:
			data_fields = []
			for i_2 in data: #take out of loop if speed becomes an issue 
				data_fields.append(i[i_2])
			try:
				self.dbase_add(data_fields, columns, dbase, table)
			except:
				self.__tba_fail_lst.append(i)
				print("{0} was not added to the database.".format(i["Product Name"]))

			else:
				print("{0} was added to table \"{1}\" in databse \"{2}\" ".format(i["Product Name"], table, dbase))

	def add_prod_cat_def(self, target_cat, attrs, image_folder="C:\\Users\\Owner\\Desktop\\I\\"):
		#adds a single product to a single category (id)
		attrs = d_copy(attrs)
		def_image = "C:\\Users\\Owner\\Desktop\\I\\Card Backs & Logos\\no-image.jpg"
		assert type(target_cat) == int, "{0} must be int".format(target_cat)
		assert type(attrs) == dict, "{0} must be dict".format(attrs)
		self.driver.get("https://catalog.crystalcommerce.com/categories/{0}".format(target_cat))
		self.driver.execute_script(
			'''
			var f = document.getElementsByClassName('control-group')[0];
			for (i = 0 ; i < f.children.length ; i++){
			if (f.children[i].innerHTML == "New Product"){
      			f.children[i].click();
			}
			else{
    			console.log("DID NOT FIND IT");
			}}'''
			)

		while self.driver.execute_script('return document.readyState') != "complete":
			#this is here to prevent the product name from being added before the page is finished loading
			time.sleep(.1)
		start = self.driver.current_url
		
		
		keys = list(attrs.keys())
		if "Product Name" not in keys:
			raise Crit_not_present("Product Name desciptor not found")
		if "Category" not in keys:
			raise Crit_not_present("Category id not present")
		self.crit_find("Product Name", attrs["Product Name"])
		if "Manufacturer SKU" in keys:
			self.crit_find("Manufacturer SKU", attrs["Manufacturer SKU"])
		#product name must be added first in order to prevent it from being overridden by unneccessary/improper descriptors (e.g. "Name")
		keys_added = ['Category', 'Product Name', 'Manufacturer SKU', 'Product Image']
		#TESTING ONLY REMOVE LATER#########################
		#print("ADDING CRITS!")
		for i in range(0, len(keys)):

			if keys[i] not in keys_added:
				#print("Adding {0}".format(str(keys[i])))
				self.crit_find(keys[i], attrs[keys[i]])
		#need to add image loader here
		photo_name = attrs.get('Product Image', def_image)
		b_list = [def_image, '']
		if photo_name not in b_list:
			photo_path = image_folder + photo_name
			check = self.add_image(photo_path)
			if not check:
				attrs['Photo Present'] = 0
			else:
				attrs['Photo Present'] = 1
		self.driver.execute_script(
			'''
			var items = document.getElementsByTagName('*');
			for (i = 0; i < items.length ; i++){
   					if ( items[i].value == "Create Product"){
        			var result = items[i] ;
        			result.click();
			}}''')
		while self.driver.execute_script('return document.readyState') != "complete" or self.driver.current_url == start:
			time.sleep(.5)
			#needs exception handling in order to catch any kickback from server regarding duplicate barcodes and/or ASINs
		final_url = self.driver.current_url
		product_id = fn_grab(final_url)
		attrs["Product Id"] = product_id
		self.__add_list.append(attrs) #adds attrs to __add_list
		entry_maker([attrs["Product Name"]]) 
		dbase_info = ''
		#creates a log entry for the product (ideally this should happen in bulk after all items have been added)
		print(attrs)#only for testing
		return attrs
	def dbase_q_form(self, x):
		#used to prepare values before they are entered into a sql database
		data = x

		data = data.replace('"', '\\"')
		data = data.replace("'", "\\'")
		return data

	def dbase_add(self, data, columns, dbase, table):
		self.dbObject.cust_com("Use {0};".format(dbase))
		#data = [re.sub('"', '\"', str(i)) for i in data]
		#data = [re.sub("'", '\'', str(i)) for i in data]
		row_values = '('
		for i in range(0, len(data)):
			if i == len(data) - 1:
				row_values += "\"" + self.dbase_q_form(str(data[i])) + "\"" + ')'
			else:
				row_values += "\"" + self.dbase_q_form(str(data[i])) + "\"" + ', '
		column_values = '('
		for i in range(0, len(columns)):
			if i == len(columns) - 1:
				column_values += str(columns[i]) + ')'
			else:
				column_values += str(columns[i]) + ', '
		full_com = "INSERT into {0} {1} VALUES {2}".format(table, column_values, row_values)
		self.dbObject.cust_com(full_com)
		return full_com
	def dbase_dupe_check(self, dbase, table, column, x):
		self.dbObject.cust_com("Use {0};".format(dbase))

		resp = self.dbObject.query("SELECT {1} FROM {0} WHERE {1} = \"{2}\"".format(table, column, self.dbase_q_form(str(x))))
		if resp[0] == x:
			return True
		else:
			return False
	def cat_dupe_check(self, data, cats = True):
		results = []
		non_dupe = []
		for i in data:
			#name = self.dbase_q_form(i["Product Name"])
			if cats:
				res = self.cat_dbase.is_in_cat("name", self.dbase_q_form(i["Product Name"]), i["Category"])
			else:
				res = self.cat_dbase.is_in_cat("name", self.dbase_q_form(i["Product Name"]))
			if res and cats:
				prod = self.cat_dbase.query("SELECT id FROM products WHERE name = \"{0}\" AND category_id = \"{1}\";".format(self.dbase_q_form(i["Product Name"]), i["Category"]))
				if len(prod) > 1:
					print("{0} is already in catalog (multiple times in fact) (See: {1})".format(self.dbase_q_form(i["Product Name"]), str(prod[0][0])))
				else:
					print("{0} is already in catalog (See: {1})".format(self.dbase_q_form(i["Product Name"]), str(prod[0][0])))

				results.append(i)
			elif res and not cats:
				prod = self.cat_dbase.query("SELECT id FROM products WHERE name = \"{0}\";".format(self.dbase_q_form(i["Product Name"])))
				if len(prod) > 1:
					print("{0} is already in catalog (multiple times in fact) (See: {1})".format(self.dbase_q_form(i["Product Name"]), str(prod[0][0])))
				else:
					print("{0} is already in catalog (See: {1})".format(self.dbase_q_form(i["Product Name"]), str(prod[0][0])))

				results.append(i)
			else:
				non_dupe.append(i)


		self.__duplicates = results
		return non_dupe



	def add_prod_cat_batch(self, cats = True, log = 0):
		results = []
		results_names = []
		pcheck_list = []
		failure_list = []
		self.__duplicates = []
		items = self.fname
		#checks for errors
		for i in range(0, len(items)):
			try:
				self.error_check(items[i])
			except Crit_not_present as CnP:
				pcheck_list.append(S_format(items[i]).d_sort())
		if pcheck_list != []:
			print('Product Name or Category ID were not found in one or more of the items')
			return pcheck_list
		#checks for duplicates if __dupe_check is True
		if self.__dupe_check:
			non_dupes = self.cat_dupe_check(items, cats)

			'''for i in items:
				if self.dbase_dupe_check('preorders', 'adds', 'product_name', i["Product Name"]):
					product_id = self.dbaseObject.query("SELECT {1} FROM {0} WHERE {3} = \"{2}\"".format('adds', 'product_id', self.dbase_q_form(str(i["Product Name"])), "product_name"))

					print("\"{0}\" is a duplicate of Product #{1} in the catalog".format(i["Product Name"], product_id[0][0]))
					self.__duplicates.append(i)'''
		if self.__duplicates != []:
			response = input("Duplicates detected. Do you wish to add only the non-duplicates? (Y/N) ")
			if response not in ['y', 'Y', 'yes']:
				raise Duplicate_Detected("Duplicates detected. If you wish to proceed, please remove all the duplicate items or set the system to ignore duplicates")
			else:
				items = non_dupes
		#proceeds to create the items
		for i in range(0, len(items)):
			try:
				confirm = self.add_prod_cat_def(int(items[i]['Category']), items[i])
			except KeyboardInterrupt as KE:
				break
			except:
				print("ERROR HAS OCCCURED")
				print(sys.exc_info()[:])
				#neeeds to be more specific
				failed_item = S_format(items[i]).d_sort()
				failure_list.append(failed_item)

			else:
				if confirm['Product Id'] == "products":
					self.__fail_lst.append(items[i])
					failure_list.append(list(S_format(items[i]).d_sort()))
				else:
					results.append(list(confirm.values()))
					results_names.append(confirm['Product Name'])
					#for testing only,   ideally this should make an entry into a database
		w_csv(results, 'batch_create.csv')
		if failure_list != []:
			print("Some items were not added due to errors. Please see fail_file.csv for more")
			w_csv(failure_list, "fail_file.csv")
		if log != 0:
			for i in range(0, len(results_names)):
				entry_maker(str(results_names[i]))
		return results
	def error_check(self, x):
		error_list = []
		assert type(x) == dict, "Argument must be dictionary."
		#checks to see if there is a product name and a category column
		keys = list(x.keys())
		if "Product Name" not in keys:
			raise Crit_not_present("Product Name desciptor not found")
		if "Category" not in keys:
			raise Crit_not_present("Category id not present")
		#checks to see if each item has a product name and a category number



	def add_image(self, image_name):
		try:
			photo_element = self.driver.find_element_by_id('product_photo')
		except:
			return False
		photo_element.send_keys(image_name)
	def update_image(self, prod_id, image_name):
		assert type(prod_id) == int, "Product Id must be int"
		start = self.driver.current_url
		url = 'https://catalog.crystalcommerce.com/products/' + str(x) + '/edit'
		self.driver.get(url)
		while load_check(start):
			time.sleep(.3)
		self.add_image(image_name)

	def load_check(self, start):
		#takes initial url (url of page before request) as argument

		if self.driver.execute_script('return document.readyState') != "complete" and self.driver.current_url == start:
			return True
		else:
			return False


	def crit_find(self, crit, value):
		#should use a function in the future
		#also needs exception handling
		value = str(value).strip(' ')
		value = re.sub("'", "\\\'",  value)
		value = re.sub('"', '\\\"', value)
		#print("Attempting to set {0} to \"{1}\"".format(str(crit), str(value)))

		command = '''
			var p_type = document.getElementsByTagName('legend')[0].innerHTML;

			var items = document.getElementsByTagName('label');
			for (i = 0; i < items.length; i++){{
				var ind_item  = items[i].innerHTML;
				if (p_type.includes('Board Games Product') && ind_item.includes('Publisher') && '{0}' == 'Publisher') {{

					items[i].nextElementSibling.value = '{1}';

				}}
				else if (ind_item.includes('{0}') && items[i].nextElementSibling.children[0].value == '') {{
					var t_item  = items[i].nextElementSibling.children[0];
					t_item.value = '{1}' ; 
				}}
				}}
			'''.format(crit, value)
		self.driver.execute_script(command)






test_d = {"Product Name":'  Captain America - 1', "MSRP":'5.99', 'Barcode/UPC': '1337', 'Manufacturer SKU':'TEST 01', 'Category': 22054}



def dictionarify(x):
	#should produce list of dictionaries from a csv, with the column headers as the keys
	item = C_sort(x)
	items = item.contents
	crit = item.contents[0]
	results = []
	for i in range(1, len(items)):
		d = dict.fromkeys(crit, 0)
		for i_2 in range(0, len(items[i])):
			d[crit[i_2]] = items[i][i_2]
		results.append(d)
	return results



#test_inst = Cat_session()
#test_inst.start()
#time.sleep(5)
#test_inst.delete_product_single(6317013)
#time.sleep(2)
#test_add.add_prod_cat_def(21333, test_d)
#test_add.add_prod_cat_batch('test_csv.csv')

'''test_add = Cat_product_add()
test_add.start()
'''

if len(sys.argv) > 1:
	if sys.argv[1] == '-t':
		print(sys.argv[2])
		splitter(sys.argv[2])
	elif sys.argv[1] == '-s':
		main_imp(sys.argv[2],sys.argv[3])
else:
	print("[data]")



class Crit_not_present(Exception):
	pass
class Duplicate_Detected(Exception):
	pass



def descriptor_get(x):
	#returns the every descriptor on the product page as a dictionary
	#takes beautifulsoup object
	d = {}
	bsObject = x
	pi_page = x.find('div', {'class':'product'})
	#default descriptors
	d["Product Name"] = pi_page.find('h2', {'class':'product_name'}).text
	d["Product Type"] = pi_page.find('h4', {'class': 'product_type_name'}).a.text
	#finding the image
	image_col = bsObject.find('div', {'class':'span4'})
	image_rows = image_col.find_all('li')
	image_link_element = image_rows[0].find('a',{'class':'thumbnail'})
	image_link = 'https:' + S_format(str(image_link_element)).linkf('href=').split('?')[0]
	d["Product Image Link"] = image_link
	d["Product Image"] = fn_grab(image_link) 
	table = pi_page.find('table')
	rows = table.find_all('tr')
	for i in range(0, len(rows)):
		d[rows[i].find('th').text] = rows[i].find('th').find_next('td').text
	#unique descriptors (i.e. the descriptors of the product type)
	desc_table = pi_page.find('table', {'id':'product_descriptors'}).tbody
	desc_rows = desc_table.find_all('tr')
	for i in range(0, len(desc_rows)):
		d[desc_rows[i].find('th').text] = desc_rows[i].find('th').find_next('td').text
	return d

def date_form():
    #returns the current date in the YYYY-MM-DD HH:MM:SS required by the datetime data type in mysql
    full_dt = time.localtime()
    year = str(full_dt[0])
    month = leading_zero(full_dt[1],2)
    day = leading_zero(full_dt[2], 2)
    hour = leading_zero(full_dt[3],2)
    minutes = leading_zero(full_dt[4], 2)
    seconds = leading_zero(full_dt[5],2)
    date_time = "{0}-{1}-{2} {3}:{4}:{5}".format(year, month, day, hour, minutes, seconds)
    return date_time
def leading_zero(x, length):
    if len(str(x)) < length:
        return "0" + str(x)
    else:
        return str(x)




def j_script(x,target, atr_val):

			'''

			for (i = 0 ; i < f.children.length ; i++){
			if (f.children[i]. == "New Product"){
      			f.children[i].click();
			}
			else{
    			console.log("DID NOT FIND IT");
			}}'''
			

def add_barcodes(bcodes):
	x = Cat_product_add()
	for i in bcodes:
		info = [i, date_form()]
		x.dbase_add(info, ["barcode", "date_added"], "asins", "barcodes")
	print("Done")
	x = ''


def add_preorders(x, dupe_check = True):
	cat_inst = Cat_product_add()
	cat_inst.set_dupe_check(dupe_check)
	cat_inst.start_browser()
	time.sleep(3)
	cat_inst.start()
	image_check = dictionarify(x)
	for i in image_check:
		check = i["Product Image"]
		check = i["Product Name"]
		check = i["Manufacturer SKU"]
		try:
			i["Year"]
		except KeyError:
			i["Year"] = str(time.localtime()[0])
	cat_inst.fname = dictionarify(x)
	cat_inst.add_prod_cat_batch()
	items = cat_inst.get_addlst()
	columns = ['product_name', 'product_id', 'sku', 'manufacturer', 'category_id', 'date_added']

	for i in items:
		if i["Product Id"].isdigit():
			info = [i["Product Name"], i["Product Id"], i.get('Manufacturer SKU', ''), i.get("Manufacturer", ''), i.get("Category", ''), date_form()]
			try:
				cat_inst.dbase_add(info, columns, 'preorders','adds' )
			except:
				
				print("Failed to add {0}".format(i["Product Name"]))
			else:
				print("Added {0} to database.".format(i["Product Name"]))

	return "Complete"
def add_items(x, session = ''):
	if session != '':
		cat_inst = session
	else:
		cat_inst = Cat_product_add()
	cat_inst.start()
	cat_inst.add_prod_cat_batch(x)
	return cat_inst.get_addlst()

def test_add_f(fname, ignore_p_id = False):
	test_add = Cat_product_add()
	test_add.set_tba_list(fname)
	test1 = test_add.get_tba_list()

	for i in test1:
		i["Dtime"] = date_form()
		if ignore_p_id:
			i["Product Id"] = "0000000"
			i["Manufacturer"]
	headers = test_add.dbObject.retr_columns('adds')
	test_add.submit_tbalst(["Product Name", "Product Id", "Manufacturer SKU", "Manufacturer", "Category", "Dtime"], headers, 'preorders', 'adds')
#test_add_f()