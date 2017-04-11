#search result normalizer
#for string
import re
class Norm_str:
	def __init__(self, text):
		self.text = text
		self.__generic = []
	def __eq__(self, x):
		#takes other Norm_str object
		if self.normify() == x.normify():
			return True
		else:
			return False
	def get_gen_lst(self):
		return self.__generic
	def set_gen_lst(self, x):
		if not isinstance(x, list):
			raise TypeError("Param must be list")
		else:
			self.__generic = x
	def normify(self):
		new_text = self.text
		#first remove all generic phrases and words from text
		for i in self.__generic:
			new_text = re.sub(str(i), '', new_text)
		#next it fixes the text capitalization
		new_text = new_text.lower()
		#next it removes any excess spaces
		new_text = self.space_norm(new_text)
		return new_text
	def space_norm(self, x):
		new_text = x.split(' ')
		if len(new_text) == 1:
			#if there are no spaces it simply returns the original string
			return x
		else:
			while '' in new_text:
				new_text.remove('')
			new_text = ' '.join(new_text)
			return new_text
'''test_1 = "TEST Product: Number One"
test_2 = "Test Product - number one"
print("Result pre-normalization:", test_1 == test_2 )
test_3 = Norm_str(test_1)
test_4 = Norm_str(test_2)
gen = ["-", ":"]
test_3.set_gen_lst(gen)
test_4.set_gen_lst(gen)
print("Result post-normalization:", test_3 == test_4 )'''


		
