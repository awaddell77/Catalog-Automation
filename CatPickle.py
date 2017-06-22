#pickle class for catalog automation
import pickle

class CatPickle:
	def __init__(self, **kwargs):
		self.data = []
		self.w_mode = "wb"
		self.r_mode = "rb"
		self.__fname = 'savefile.p'
		self.__dir = ''
	def get_fname(self):
		return self.__fname
	def get_dir(self):
		return self.__dir

	def set_fname(self, x):
		if not isinstance(x, str):
			raise TypeError("Argument must be str.")
		else:
			self.__fname = x
			
	def set_dir(self, x):
		if not isinstance(x, str):
			raise TypeError("Argument must be str.")
		else:
			self.__dir = x

	def save_obj(self, x):
		self.data = x


test = CatPickle()
