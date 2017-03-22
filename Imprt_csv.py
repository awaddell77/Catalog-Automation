from soupclass8 import *
class Imprt_csv:
	def __init__(self, x, req_crits,  dir_n = "C:\\Users\\Owner\\Desktop\\I\\"):
		self.fname = dictionarify(x)
		self.dir_n = dir_n
		self.req_crits = req_crits


	def check_for_issues(self, allow_empty = []):
		new_x = self.fname
		crits = self.req_crits
		for i_2 in range(0, len(new_x)):
			photo_error = False


			#checks to see if Image Link is present if Product Image field is not, then creates a product image field by extracting the file name from the url
			if "Product Image" not in list(new_x[i_2].keys()) and "Image Link" in list(new_x[i_2].keys()):
				new_x[i_2]["Product Image"] = fn_grab(new_x[i_2]["Image Link"])

			#by default this method allows empty fields, if allow_empty is a list or tuple then it will allow empty fields in all categories except for those listed under allow_empty argument
			#needs to be more elegant
			if allow_empty != []:
				for cats in allow_empty:
					if self.empty_check(new_x[i_2], cats):
						raise Crit_not_present("The {0} field in item #{1} was left blank.".format(str(cats), str(i_2)))
				empty_field = False

			for i in range(0, len(crits)):
				#checks each dict to see if they have the necessary fields
				req_field_pres = crits[i] not in list(new_x[i_2].keys())
				missing_crit = self.ke_check(new_x[i_2], crits[i])
				if allow_empty == []:
					empty_field = False




				if req_field_pres or missing_crit or empty_field:
					if req_field_pres and new_x:
						raise Crit_not_present("CSV is missing a required field: {0}".format(crits[i]))
					if missing_crit:
						raise Crit_not_present("Item #{0} is missing a required field: {1}".format(str(i_2), crits[i]))
					if empty_field:
						raise Crit_not_present("The {0} field in item #{1} was left blank.".format(crits[i], str(i_2)))
			#checks to see if fields contain appropriate content (i.e. the correct type of data)
			if '.gif' in new_x[i_2].get("Product Image", ''): photo_error = True 
			if photo_error:
				raise Value_not_appr("Product Image \"{0}\" for Item #{1} (Product Name: {2}) is an invalid file type (gif)".format(new_x[i_2]["Product Image"], str(i_2), new_x[i_2]["Product Name"]))
			if not self.image_check(new_x[i_2].get("Product Image", '')) and "Product Image" not in allow_empty and new_x[i_2].get("Product Image", '') not in ['', ' ']:
				raise Image_not_found("Image file {0} not found in directory {1}".format(new_x[i_2]["Product Image"], self.dir_n))
		return new_x

	def ke_check(self, x, key):
		#returns true for key errors
		try:
			x[key]
		except KeyError as KE:
			return True
		else:
			return False
	def empty_check(self, x, key):
		#returns true if value is empty of '' AND ONLY when that is the case. If there is no such key it returns false anyways
		try:
			contents = x[key]
		except KeyError as KE:
			return False
		else:
			if contents == '':
				return True
			else:
				return False

	def number_check(self, x):
		#checks to see if barcode, product Id, MSRP are numbers. Returns True if error is detected
		try:
			int(x)
		except ValueError as VE:
			try:
				float(x)
			except ValueError as VE:
				return True
			else:
				return False
	def image_check(self, x):
		full_path = self.dir_n + x
		if os.path.exists(full_path):
			return True
		if not os.path.exists(full_path):
			return False
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
class Crit_not_present(Exception):
	pass
class Value_not_appr(Exception):
	#for when the contents are not appropriate or valid
	pass
class Image_not_found(Exception):
	#for when it cannot find the images
	pass
