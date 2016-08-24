from soupclass8 import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import getpass
import sys


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
		return bs(self.driver.page_source, 'lxml')


	def interpreter(self,*args):
		print('This is the command: %s' % (args))
		'''if 'Search' in args:
			x = args.split('')
			return self.prod_s(x[1])'''


	def start(self):#login method
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
			#all_in_checkbox = self.driver.execute_script('return document.getElementById("product_variation_category_id").click()')
			checkbox.click()
			self.driver.execute_script('document.getElementById("product_variation_category_id").click()')
		except:
			print("Something went wrong")
		self.b_grab('btn btn-info','value', 'Push Skus to Clients').click()

	def push_asins(self,x):
		self.cat_goto(x)
		try:
			checkbox = self.driver.find_element_by_id('all_products')
			checkbox.click()
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

	def move_cat(self, x):
		#moves a single item to a different category
		self.prod_go_to(x + '/edit')
		categories = self.driver.execute_script('document.getElementsByClassName("select required select2 wide-category-select")[0].children')
		#clicks on the drop down menu
		self.driver.execute_script('document.getElementsByClassName("select2-offscreen select2-focusser")[0].click();')
		#once the menu has been clicked the options are now visible 


	def prod_go_to(self, x):
		url = 'https://catalog.crystalcommerce.com/products/' + x
		self.driver.get(url)

	def cat_find(self, x):
		categories = self.driver.execute_script('return document.getElementsByClassName("select required select2 wide-category-select")[0].children')
		for i in range(0, len(categories)):
			cat = categories[i].get_attribute('value')
			if x == cat:
				name self.driver.execute_script('return document.getElementsByClassName("select required select2 wide-category-select")[0].children[%s].innerHTML;' % str(i))
				return name
		return


		




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





if len(sys.argv) > 1:
	if sys.argv[1] == '-t':
		print(sys.argv[2])
		splitter(sys.argv[2])
	elif sys.argv[1] == '-s':
		main_imp(sys.argv[2],sys.argv[3])
else:
	print("[data]")







