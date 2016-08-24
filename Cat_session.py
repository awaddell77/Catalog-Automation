from soupclass8 import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import getpass




class Cat_session(object):#parent class for this pseudo-API
	def __init__(self, *args):
		self.username = input('Username:') 
		self.password = getpass.getpass('Password:')
		self.driver = webdriver.Firefox()
		#in the future allow the user to select which browser to use (would need to make this a child of a parent that did that)
		#self.driver = webdriver.PhantomJS()
		self.args = args
	def main(self):
		terminate = ['Log off','Logout', 'Exit']
		self.session_start()
		data = ''
		#return self.driver
		while data not in terminate:
			data = input('>>')
			self.interpreter(data)
	def source(self):
		return self.driver.page_source


	def interpreter(self,*args):
		print('This is the command: %s' % (args))
		'''if 'Search' in args:
			x = args.split('')
			return self.prod_s(x[1])'''


	def session_start(self):#login method
		self.driver.get('https://accounts.crystalcommerce.com/users/sign_in')
		element = self.driver.find_element_by_id('user_email')
		element1 = self.driver.find_element_by_id('user_password')
		element.send_keys(self.username)
		element1.send_keys(self.password)
		element3 = self.driver.find_element_by_name('commit')# sign in button
		element3.click()
		self.target()
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

	def push_skus(self,x):
		self.cat_goto(x)
		try:
			checkbox = self.driver.find_element_by_id('all_products')
			all_in_checkbox = self.driver.find_element_by_id('product_variation_category_id')
			checkbox.click()
		self.b_grab('btn btn-info','value', 'Push Skus to Clients').click()



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








class Cat_search(Cat_session):
	def __init__(self, *args):
		#super().__init__()
		self.args = args
		self.session_start()
	def cat_s(self, cat_name):#searches for a category (cat_name)
		element_1 = self.driver.find_element_by_link_text('Categories')#
		element_1.click()
		element_2 = self.driver.find_element_by_id('categories_search_q')
		element_2.send_keys(cat_name)#puts cat_name into the search box
		element_2.send_keys(Keys.RETURN)#using keystroke key in order to avoid accidently clicking other buttons (in case they change in the future)
		return self.driver












