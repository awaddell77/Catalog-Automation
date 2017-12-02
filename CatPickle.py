#pickle class for catalog automation
import pickle
import os

class CatPickle:
	def __init__(self, **kwargs):
		self.data = []
		self.w_mode = "wb"
		self.r_mode = "rb"
		self.__fname = kwargs.get('fname', 'savefile.p')
		self.tdir = kwargs.get('dir', '')
	def get_fname(self):
		return self.__fname
	def get_dir(self):
		if not self.tdir:
			return os.getcwd() + "\\"


		return self.tdir

	def set_fname(self, x):
		if not isinstance(x, str):
			raise TypeError("Argument must be str.")
		else:
			self.__fname = x

	def set_dir(self, x):
		if not isinstance(x, str):
			raise TypeError("Argument must be str.")
		else:
			self.tdir = x

	def save_obj(self, x):
		self.data = x
		f = open(self.get_dir() + self.__fname, self.w_mode)
		pickle.dump(self.data, f)
		f.close()
	def open_p(self, tfile):
		return pickle.load(open(self.get_dir + tfilem, self.r_mode))



test = CatPickle(dir = "C:\\Users\Owner\\Catalog-Automation\\Pickles\\")
h = ['testing', '1', '2', '3']
test.save_obj(h)
