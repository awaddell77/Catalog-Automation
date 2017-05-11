#key match
from Cat_dbase import *
class Pupdate:
	def __init__(self, category, new_info):
		self.category = category
		self.new_info = dictionarify(new_info)
	def import_doc(self, x):
		#for importing new file without having to start new instance
		self.new_info = dictionarify(x)
	
