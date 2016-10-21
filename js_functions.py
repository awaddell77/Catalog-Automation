#javascript functions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from js_lib import *

#javascript functions ("jfunctions") must be included in the methods

class Js_functions_lib(object):
	def __init__(self, session):
		self.session = session
		js_load(self.session, js_funcs)
		self.current_functions = js_funcs
		#should be the parent of Js_functions

class Js_functions(object):
	def __init__(self, session):
		self.session = session
	def find_element_by_id(self, e_id):
		function = '''
		function fb_id(x) {
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




def js_load(session, x):
	assert type(x) == list, "Argument must be a list"
	for i in range(0, len(x)):
		try:
			session.execute_script(x[i])
		except:
			"{0} failed to load".format(x[i])


functions = [
	function_fb_id = '''
		function fb_id(x) {
			var item = document.getElementById(x);
			if (item == null){
				return False;
			}
			else{
				return item;
			}

		}'''
	function_fb_cn = '''
		function fb_cn(x){
		var item = document.getElementsByClassName(x);
		if (item == null){
			return False;
			}
		else{
			return item[0]
		}
		}
		''',
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


]