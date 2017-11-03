#formatting object for dictionary objects
import random
from Im_dwnld import *
from I_handling import *

class Amzn_lst_single:
	def __init__(self, values):
		self.__values = values
		self.__game = ''
		self.__set_name = ''
		self.__manufacturer = ''
		self.__ages = '12'
		self.__dir = "C:\\Users\\Owner\\Desktop\\I\\"
		self.__d_opt = True
		self.__keywords = 'teenage boys'
		self.part_number = values.get("Card Number", random.randint(0, 100))
		if not isinstance(self.__values, dict):
			raise TypeError("Param must be dictionary.")
		self.__cat_form = False
	def __str__(self):
		return self.__values
	def get_dir(self):
		return self.__dir
	def set_dir(self, x):
		self.__dir = x
	def get_d_opt(self):
		return self.__d_opt
	def set_d_opt(self, x):
		if not isinstance(x, bool):
			raise TypeError("Argument must be bool")
		else:
			self.__d_opt = x
	def get_game(self):
		return self.__game
	def set_game(self, x):
		self.__game = x
	def get_man(self):
		return self.__manufacturer
	def set_man(self, x):
		self.__manufacturer = x
	def get_ages(self):
		return self.__ages
	def set_ages(self, x):
		self.__ages = x
	def get_keywords(self):
		return self.__keywords
	def set_keywords(self, x):
		self.__keywords = x
	def get_cat_form(self):
		return self.__cat_form
	def set_cat_form(self, x):
		if not isinstance(x, bool):
			raise TypeError("Argument must be bool")
		else:
			self.__cat_form = x
	def form(self):
		#need to have special 'filter' that prevents promo cards from getting their category names added to their amazon listing names
		if self.__values["Product Type"] == 'Yu-Gi-Oh Singles':
			self.set_game('Yu-Gi-Oh')
			self.set_man('yu-gi-oh')
			self.set_keywords('teenage boys')
			card = self.__ygo_form()
			return card
		elif self.__values["Product Type"] == "Magic Singles":
			self.set_game('Magic: The Gathering (MTG)')
			self.set_man("Wizards of the Coast")
			self.set_keywords('teenage boys')
			card = self.__mtg_form()
			return card
		elif self.__values["Product Type"] == "Cardfight!! Vanguard":
			self.set_game('Cardfight! Vanguard')
			self.set_man("Bushiroad")
			self.set_keywords('teenage boys')
			card = self.__cfv_form()
			return card
		elif self.__values["Product Type"] == "Weiss Schwarz Singles":
			self.set_game('Weiss Schwarz')
			self.set_man("Bushiroad")
			self.set_keywords('teenage boys')
			card = self.__ws_form()
			return card
		elif self.__values["Product Type"] == "Pokemon Singles":
			self.set_game('Pokémon')
			#self.set_man("The pokemon company")
			self.set_man('Pokémon Company International')
			self.set_keywords('teenage boys')
			card = self.__pkm_form()
			return card
		elif self.__values["Product Type"] == "Dragon Ball Super TCG Singles":
			self.set_game('Dragon Ball Super')
			#self.set_man("The pokemon company")
			self.set_man('Dragon Ball Super TCG')
			self.set_keywords('teenage boys')
			card = self.__dbs_form()
			return card
		elif self.__values["Product Type"] == "Dragoborne Singles":
			self.set_game('Dragoborne')
			#self.set_man("The pokemon company")
			self.set_man('Dragoborne TCG')
			self.set_keywords('teenage boys')
			card = self.__dragoborne_form()
			return card

		else:
			print("Product Type \"{0}\" is not recognized".format(self.__values["Product Type"]))
			#TODO fix this, should return same datatype (in this case, a dictionary)
	def __ygo_form(self):
		#returns dictionary containing Product Name, Product Id, MSRP, Description, Product Image, and Image Link
		#downloads the image the directory listed in the dir data field if d_opt is True
		d = {}
		card_name = self.__values["Product Name"]
		card_edition = self.__values.get("Edition", '')
		set_name = self.__values.get("Category", '')
		if not card_edition:
			#if card_edition is empty
			full_name = card_name + ' - ' + set_name
		else:
			full_name = card_name + ' - ' + set_name + ' (' + card_edition + ' Edition)'
		d["Product Name"] = full_name
		d["Product Id"] = self.__values['Product Id']
		d["MSRP"] = str(random.randint(1,301) / 100)
		d["Manufacturer"] = self.get_man()
		d["Ages"] = self.get_ages()
		d["Keywords"] = self.get_keywords()
		d["Barcode Type"] = 'ean'
		d["Part Number"] = self.part_number
		if not self.__values.get("Rarity", ''):
			d['Description'] = 'An individual card from the ' + self.get_game() + ' trading and collectible card game (TCG/CCG).'
		else:
			d['Description'] = 'An individual card from the ' + self.get_game() + ' trading and collectible card game (TCG/CCG). This is of the ' + self.__values['Rarity'] + ' rarity.'
		d["Product Image"] = self.__values["Product Image"]
		d["Image Link"] = self.__values["Product Image Link"]
		if self.get_d_opt():
			d_inst = Im_dwnld(self.__dir)
			#brackets are there because it needs to be a list
			d_inst.i_main([d["Image Link"]])
		return d
	def __mtg_form(self):
		#returns dictionary containing Product Name, Product Id, MSRP, Description, Product Image, and Image Link
		#downloads the image the directory listed in the dir data field if d_opt is True
		d = {}
		card_name = self.__values["Product Name"]
		cat_name = self.__values.get("Category", '')
		if not self.__values.get("Set Name", ''):
			#if Set Name descriptor is empty
			full_name = card_name + ' - ' + cat_name
		elif self.__values.get("Set Name", '') != cat_name:
			#if Set Name descriptor is different from category name
			full_name = card_name + ' - ' + self.__values.get("Set Name", '') + ' - (' + cat_name + ')'
		else:
			#if Set Name descriptor is the same as the category name
			full_name = card_name + ' - ' + self.__values.get("Set Name", '')

		d["Product Name"] = full_name
		d["Product Id"] = self.__values['Product Id']
		d["MSRP"] = str(random.randint(1,301) / 100)
		d["Manufacturer"] = self.get_man()
		d["Ages"] = self.get_ages()
		d["Keywords"] = self.get_keywords()
		d["Barcode Type"] = 'ean'
		d["Part Number"] = self.part_number
		if not self.__values.get("Rarity", ''):
			d['Description'] = 'An individual card from the ' + self.get_game() + ' trading and collectible card game (TCG/CCG).'
		else:
			d['Description'] = 'An individual card from the ' + self.get_game() + ' trading and collectible card game (TCG/CCG). This is of the ' + self.__values['Rarity'] + ' rarity.'
		d["Product Image"] = self.__values["Product Image"]
		d["Image Link"] = self.__values["Product Image Link"]
		if self.get_d_opt():
			d_inst = Im_dwnld(self.__dir)
			#brackets are there because it needs to be a list
			d_inst.i_main([d["Image Link"]])
		return d
	def __cfv_form(self):
		#returns dictionary containing Product Name, Product Id, MSRP, Description, Product Image, and Image Link
		#downloads the image the directory listed in the dir data field if d_opt is True
		d = {}
		card_name = self.__values["Product Name"]
		cat_name = self.__values.get("Category", '')
		if not self.__values.get("Set Name", ''):
			#if Set Name descriptor is empty
			full_name = card_name + ' - ' + cat_name
		elif self.__values.get("Set Name", '') != cat_name:
			#if Set Name descriptor is different from category name
			full_name = card_name + ' - ' + self.__values.get("Set Name", '') + ' - (' + cat_name + ')'
		else:
			#if Set Name descriptor is the same as the category name
			full_name = card_name + ' - ' + self.__values.get("Set Name", '')

		d["Product Name"] = full_name
		d["Product Id"] = self.__values['Product Id']
		d["MSRP"] = str(random.randint(1,301) / 100)
		d["Manufacturer"] = self.get_man()
		d["Ages"] = self.get_ages()
		d["Keywords"] = self.get_keywords()
		d["Barcode Type"] = 'ean'
		d["Part Number"] = self.part_number
		if not self.__values.get("Rarity", ''):
			d['Description'] = 'An individual card from the ' + self.get_game() + ' trading and collectible card game (TCG/CCG).'
		else:
			d['Description'] = 'An individual card from the ' + self.get_game() + ' trading and collectible card game (TCG/CCG). This is of the ' + self.__values['Rarity'] + ' rarity.'
		d["Product Image"] = self.__values["Product Image"]
		d["Image Link"] = self.__values["Product Image Link"]
		if self.get_d_opt():
			d_inst = Im_dwnld(self.__dir)
			#brackets are there because it needs to be a list
			d_inst.i_main([d["Image Link"]])
		return d
	def __ws_form(self):
		#returns dictionary containing Product Name, Product Id, MSRP, Description, Product Image, and Image Link
		#downloads the image the directory listed in the dir data field if d_opt is True
		d = {}
		card_name = self.__values["Product Name"]
		cat_name = self.__values.get("Category", '')
		if not self.__values.get("Set Name", ''):
			#if Set Name descriptor is empty
			full_name = card_name + ' - ' + cat_name
		elif self.__values.get("Set Name", '') != cat_name:
			#if Set Name descriptor is different from category name
			full_name = card_name + ' - ' + self.__values.get("Set Name", '') + ' - (' + cat_name + ')'
		else:
			#if Set Name descriptor is the same as the category name
			full_name = card_name + ' - ' + self.__values.get("Set Name", '')

		d["Product Name"] = full_name
		d["Product Id"] = self.__values['Product Id']
		d["MSRP"] = str(random.randint(1,301) / 100)
		d["Manufacturer"] = self.get_man()
		d["Ages"] = self.get_ages()
		d["Keywords"] = self.get_keywords()
		d["Barcode Type"] = 'ean'
		d["Part Number"] = self.part_number
		if not self.__values.get("Rarity", ''):
			d['Description'] = 'An individual card from the ' + self.get_game() + ' trading and collectible card game (TCG/CCG).'
		else:
			d['Description'] = 'An individual card from the ' + self.get_game() + ' trading and collectible card game (TCG/CCG). This is of the ' + self.__values['Rarity'] + ' rarity.'
		d["Product Image"] = self.__values["Product Image"]
		d["Image Link"] = self.__values["Product Image Link"]
		if self.get_d_opt():
			d_inst = Im_dwnld(self.__dir)
			#brackets are there because it needs to be a list
			d_inst.i_main([d["Image Link"]])
			image = I_handling(self.__dir + d["Product Image"])
			image.resize((250, 322))
		return d

	def __pkm_form(self):
		#returns dictionary containing Product Name, Product Id, MSRP, Description, Product Image, and Image Link
		#downloads the image the directory listed in the dir data field if d_opt is True
		d = {}
		card_name = self.__values["Product Name"]
		cat_name = self.__values.get("Category", '')
		if not self.__values.get("Set Name", ''):
			#if Set Name descriptor is empty
			full_name = card_name + ' - ' + cat_name
		elif self.__values.get("Set Name", '') != cat_name:
			#if Set Name descriptor is different from category name
			full_name = card_name + ' - ' + self.__values.get("Set Name", '') + ' - (' + cat_name + ')'
		else:
			#if Set Name descriptor is the same as the category name
			full_name = card_name + ' - ' + self.__values.get("Set Name", '')

		d["Product Name"] = full_name
		d["Product Id"] = self.__values['Product Id']
		d["MSRP"] = str(random.randint(1,301) / 100)
		d["Manufacturer"] = self.get_man()
		d["Ages"] = self.get_ages()
		d["Keywords"] = self.get_keywords()
		d["Barcode Type"] = 'ean'
		d["Part Number"] = self.part_number
		if not self.__values.get("Rarity", ''):
			d['Description'] = 'An individual card from the ' + self.get_game() + ' trading and collectible card game (TCG/CCG).'
		else:
			d['Description'] = 'An individual card from the ' + self.get_game() + ' trading and collectible card game (TCG/CCG). This is of the ' + self.__values['Rarity'] + ' rarity.'
		d["Product Image"] = self.__values["Product Image"]
		d["Image Link"] = self.__values["Product Image Link"]
		if self.get_d_opt():
			d_inst = Im_dwnld(self.__dir)
			#brackets are there because it needs to be a list
			d_inst.i_main([d["Image Link"]])
		return d
	def __dbs_form(self):
		#returns dictionary containing Product Name, Product Id, MSRP, Description, Product Image, and Image Link
		#downloads the image the directory listed in the dir data field if d_opt is True
		d = {}
		card_name = "Dragon Ball Super TCG - " + self.__values["Product Name"]
		cat_name = self.__values.get("Category", '')
		if not self.__values.get("Set Name", ''):
			#if Set Name descriptor is empty
			full_name = card_name + ' - ' + cat_name
		elif self.__values.get("Set Name", '') != cat_name:
			#if Set Name descriptor is different from category name
			full_name = card_name + ' - ' + self.__values.get("Set Name", '') + ' - (' + cat_name + ')'
		else:
			#if Set Name descriptor is the same as the category name
			full_name = card_name + ' - ' + self.__values.get("Set Name", '')
		if self.__values["Card Number"] not in full_name and self.__values["Card Number"]:
			full_name += " - " + self.__values["Card Number"]

		d["Product Name"] = full_name
		d["Product Id"] = self.__values['Product Id']
		d["MSRP"] = str(random.randint(1,301) / 100)
		d["Manufacturer"] = self.get_man()
		d["Ages"] = self.get_ages()
		d["Keywords"] = self.get_keywords()
		d["Barcode Type"] = 'ean'
		d["Part Number"] = self.part_number
		if not self.__values.get("Rarity", ''):
			d['Description'] = 'An individual card from the ' + self.get_game() + ' trading and collectible card game (TCG/CCG).'
		else:
			d['Description'] = 'An individual card from the ' + self.get_game() + ' trading and collectible card game (TCG/CCG). This is of the ' + self.__values['Rarity'] + ' rarity.'
		d["Product Image"] = self.__values["Product Image"]
		d["Image Link"] = self.__values["Product Image Link"]
		if self.get_d_opt():
			d_inst = Im_dwnld(self.__dir)
			#brackets are there because it needs to be a list
			d_inst.i_main([d["Image Link"]])
		return d

	def __dragoborne_form(self):
		#returns dictionary containing Product Name, Product Id, MSRP, Description, Product Image, and Image Link
		#downloads the image the directory listed in the dir data field if d_opt is True
		d = {}
		card_name = self.__values["Product Name"]
		cat_name = self.__values.get("Category", '')
		if not self.__values.get("Set Name", ''):
			#if Set Name descriptor is empty
			full_name = card_name + ' - ' + cat_name
		elif self.__values.get("Set Name", '') != cat_name:
			#if Set Name descriptor is different from category name
			full_name = card_name + ' - ' + self.__values.get("Set Name", '') + ' - (' + cat_name + ')'
		else:
			#if Set Name descriptor is the same as the category name
			full_name = card_name + ' - ' + self.__values.get("Set Name", '')

		d["Product Name"] = full_name
		d["Product Id"] = self.__values['Product Id']
		d["MSRP"] = str(random.randint(1,301) / 100)
		d["Manufacturer"] = self.get_man()
		d["Ages"] = self.get_ages()
		d["Keywords"] = self.get_keywords()
		d["Barcode Type"] = 'ean'
		d["Part Number"] = self.part_number
		if not self.__values.get("Rarity", ''):
			d['Description'] = 'An individual card from the ' + self.get_game() + ' trading and collectible card game (TCG/CCG).'
		else:
			d['Description'] = 'An individual card from the ' + self.get_game() + ' trading and collectible card game (TCG/CCG). This is of the ' + self.__values['Rarity'] + ' rarity.'
		d["Product Image"] = self.__values["Product Image"]
		d["Image Link"] = self.__values["Product Image Link"]
		if self.get_d_opt():
			d_inst = Im_dwnld(self.__dir)
			#brackets are there because it needs to be a list
			d_inst.i_main([d["Image Link"]])
			image = I_handling(self.__dir + d["Product Image"])
			image.resize((250, 322))
		return d
