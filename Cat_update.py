from Cat_session import *
from Imprt_csv import *

class Cat_update(Cat_session):
	def __init__(self, update_data='', req_crits=["Product Id"], req_not_empty = [] ):
		super().__init__()
		self.session = self.driver
		self.__tbu_lst = []
		self.__updated_lst = []
		self.__fail_lst = []
		if '.csv' in update_data:
			self.item_lst = Imprt_csv(update_csv, req_crits)
			self.item_lst.check_for_issues(req_not_empty)
			self.dir_n = self.item_lst.dir_n
		else:
			self.item_lst = update_data
			self.dir_n = ''

		
	def update_data_check(self, fields=[]):
		if "Product Id" not in fields:
			fields.append("Product Id")
		for i in range(0, len(self.item_lst)):
			if type(self.item_lst[i]) != dict:
				raise TypeError("Item #{0} is not a dict".format(str(i)))
			for i_2 in fields:
				try:
					self.item_lst[i][i_2]
				except KeyError:
					raise KeyError("The \"{0}\" field is missing from item #{1}".format(str(i_2), str(i)))




	def get_tbu_lst(self):
		return self.__tbu_lst
	def set_tbu_lst(self, x):
		self.__tbu_lst = x
	def get_updated_lst(self):
		return self.__updated_lst
	def set_updated_lst(self, x):
		self.__updated_lst = x
	def get_fail_lst(self):
		return self.__fail_lst
	def set_fail_lst(self, x):
		self.__fail_lst = x

	def load_check(self, start=''):
		#takes initial url (url of page before request) as argument
		if start == '' and self.session.execute_script('return document.readyState') != "complete":
			return True
		elif start == '' and self.session.execute_script('return document.readyState') == "complete":
			return False

		elif self.session.execute_script('return document.readyState') != "complete" and self.session.current_url == start:
			return True
		else:
			return False
	def click_update(self):
		try:
			self.session.execute_script(
				'''
				var items = document.getElementsByTagName('*');
				for (i = 0; i < items.length ; i++){
						if ( items[i].value == "Update Product"){
	    				var result = items[i] ;
	    				result.click();
	    		}}''')
		except:
			return False
		else:
			return True
	def update_single_product(self, id):
		pass

	def update_descriptor_all(self, descriptor, value):
		#sorts through all descriptors and replaces values with value parameter 
		#also needs exception handling
		value = str(value).strip(' ')
		value = re.sub("'", "\\\'",  value)
		value = re.sub('"', '\\\"', value)

		command = '''
			var items = document.getElementsByTagName('label');
			for (i = 0; i < items.length; i++){{
				var ind_item  = items[i].innerHTML;
				if (ind_item.includes('{0}') && items[i].nextElementSibling.children[0].value == '') {{
					items[i].nextElementSibling.children[0].value = '{1}' ; 
				}}
				}}
			'''.format(descriptor, value)
		self.session.execute_script(command)
		return True
	def update_product_descriptor(self, descriptor, value):
		#sorts through only those descriptors that are specific to the product type
		#replaces values even if something is already in the value field
		value = str(value).strip(' ')
		value = re.sub("'", "\\\'",  value)
		value = re.sub('"', '\\\"', value)

		command = '''
			var items = document.getElementsByClassName('control-group string optional product_product_descriptors_value');
			for (i = 0; i < items.length; i++){{
				var ind_item  = items[i].children[0];
				if (ind_item.innerHTML == {0}) {{
					items[i].nextElementSibling.children[0].value = '{1}' ; 
				}}
				}}
			'''.format(descriptor, value)
		self.session.execute_script(command)


	def image_update(self, image):

		try:
			photo_element = self.session.find_element_by_id('product_photo')
		except:
			#self.__fail_lst.append(d_w_image)
			return False
		try:
			photo_element.send_keys(image)
		except:
			#self.__fail_lst.append(d_w_image)
			return False
		else:
			return True
	def go_to(self, x):
		url = 'https://catalog.crystalcommerce.com/products/' + x + '/edit'
		self.session.get(url)
		while self.load_check():
			time.sleep(.1)
		return True


	def update_images(self):
		self.__fail_lst = []
		self.__updated_lst = []
		update_items = self.item_lst.fname
		for i in range(0, len(update_items)):
			go_to_res = self.go_to(update_items[i]["Product Id"])
			go_to_upd = self.image_update(self.dir_n + update_items[i]["Product Image"])
			if not go_to_res or not go_to_upd:
				print("Failed to add item #{0} (\"{1}\")".format(str(i), update_items[i]["Product Image"]))
				self.__fail_lst.append(update_items[i])
			else:
				url = self.session.current_url
				self.click_update()
				while self.load_check(url):
					time.sleep(1)
				self.__updated_lst.append(update_items[i])
		if self.__fail_lst != [] and self.__updated_lst != []:
			print("The program encountered some issues while attempting to update some of the items in the CSV.")
			print(self.__fail_lst)
		elif self.__fail_lst !=[] and self.__updated_lst == []:
			print("The program was unable to update the items in the CSV")
		else:
			print("Successfully updated the items in the CSV")
	def update_asins(self):
		self.__fail_lst = []
		self.__updated_lst = []
		update_items = self.item_lst.fname
		for i in range(0, len(update_items)):
			go_to_res = self.go_to(update_items[i]["Product Id"])
			go_to_upd = self.update_descriptor_all('Asin', update_items[i]["ASIN"])
			if not go_to_res or not go_to_upd:
				print("Failed to add item #{0} (\"{1}\")".format(str(i), update_items[i]["ASIN"]))
				self.__fail_lst.append(update_items[i])
			else:
				url = self.session.current_url
				self.click_update()
				while self.load_check(url):
					time.sleep(1)
				self.__updated_lst.append(update_items[i])
		if self.__fail_lst != [] and self.__updated_lst != []:
			print("The program encountered some issues while attempting to update some of the items in the CSV.")
			print(self.__fail_lst)
		elif self.__fail_lst !=[] and self.__updated_lst == []:
			print("The program was unable to update the items in the CSV")
		else:
			print("Successfully updated the items in the CSV")

#test
#cat_inst = Cat_update("raging_temp_upd.csv")
#cat_inst.start()
#time.sleep(3)
#cat_inst.update_images()




