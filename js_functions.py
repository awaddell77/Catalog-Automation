#javascript functions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from js_lib import *
import re
#javascript functions ("jfunctions") must be included in the methods
test = webdriver.Firefox()
test.get('https://www.mozilla.org/en-US/contribute/')
class Js_functions_lib:
	def __init__(self, session):
		self.session = session
		js_load(self.session, js_funcs)
		self.js_funcs = js_funcs
		#should be the parent of Js_functions

class Js_functions(Js_functions_lib):
	def __init__(self, session):
		self.session = session
		Js_functions_lib.__init__(self,self.session)
	def find_element_by_id(self, e_id):
		function_t = '''function fb_id(x) {
			var item = document.getElementById(x);
			if (item == null){
				return False;
			}
			else{
				return item;
			}

		}'''
		self.session.execute_script(function)
		item = self.session.execute_script('fb_id({0})'.format(e_id))
		return item
	def find_element_by_class(self, e_cn, var = 'f_item'):
		function = '''
		function fb_cn(x){
		var item = document.getElementsByClassName(x);
		if (item == null){
			return False;
			}
		else{
			return item[0]
		}
		}
		'''
		self.session.execute_script(function)
		item = self.session.execute_script('fb_cn({0})'.format(e_cn))
		return item
	def find_elements_by_class(self, e_cn):
		function_fb_cn_m = '''
		function fb_cn_m(x){
		var item = document.getElementsByClassName(x);
		if (item == null){
			return False;
			}
		else{
			return item
		}
		}
		'''
	def remove_element(self, element):
		pass


def js_cleanse(x):
	new = x.split('\n')
	#next need to remove \t from string
	new_2 = [re.sub('\t', '', new[i]) for i in range(0, len(new))] 
	#produces a list of each line in a js function
	return new_2
def js_execute(session, x):
	#executes a js function or code snippet line by line (x must be a list)
	for i in range(0, len(x)):
		if x[i] != '':
			session.execute_script(x[i])

def js_load(session, x):
	assert type(x) == list, "Argument must be a list"
	for i in range(0, len(x)):
		try:
			#session.execute_script(x[i])
			js_execute(session, js_cleanse(x[i]))
		except:
			"{0} failed to load".format(x[i])
	print("Executed Script")

test_inst = Js_functions(test)
js_execute(test_inst.session, js_cleanse(fb_tn))