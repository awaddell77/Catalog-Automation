from Cat_session import *
import copy, random
main_csv = ["item_type", "item_sku", "external_product_id", "external_product_id_type", "item_name", "brand_name", "manufacturer", "mfg_minimum", "mtg_minimum_unit_of_measure", "product_description", "main_image_url", "target_audience_keywords", "bullet_point1",	"bullet_point2", "bullet_point3", "generic_keywords"]
def_d1 = {"item_type":"collectible-single-trading-cards", "item_sku":'', "external_product_id":'', "external_product_id_type":"EAN",
 "item_name":'', "brand_name":"Magic the Gathering", "manufacturer":"Wizards of the Coast", "mfg_minimum":'12', "mtg_minimum_unit_of_measure":'',
  "product_description":'', "main_image_url":'', "target_audience_keywords":'teenage boys',
  "bullet_point1":'',	"bullet_point2":'', "bullet_point3":'', "generic_keywords":''}
 def_d = {"item_type":"collectible-single-trading-cards", "Product Id":'', "external_product_id":'', "external_product_id_type":"EAN",
 "item_name":'', "brand_name":"Magic the Gathering", "Manufacturer":"Wizards of the Coast", "Ages":'12', "mtg_minimum_unit_of_measure":'',
  "Description":'', "Product Image":'', "Keywords":'teenage boys',
  "bullet_point1":'',	"bullet_point2":'', "bullet_point3":'', "generic_keywords":''}

browser = Cat_session()
browser.start()
time.sleep(3)
#this is the main browser object that will be used to pull picture links from the catalog
class Main(object):
	def __init__(self, fname, barcodes, **kwargs):
		self.f_contents = dictionarify(fname)
		self.barcodes = r_csv(barcodes)
		self.params = kwargs
		self.last_info = []
	def g_info(self):
		#needs to
		results = []
		for i in range(0, len(self.f_contents)):
			name_d = self.params.get('Name_d', "Name")
			prod_name = self.params.get('Product Name')
			def_tcg = "Magic: the Gathering (MTG)"
			new_d = copy.deepcopy(def_d)
			new_d["Product Name"] = self.f_contents[i].get("Product Name", 'N/A') + ' - ' + self.f_contents[i].get('Set Name', 'N/A')
			#new_d["brand_name"] = self.params.get('TCG', def_tcg)
			#new_d["manufacturer"] = self.params.get('Man', new_d["manufacturer"])
			browser.prod_go_to(self.f_contents[i]['Product Id'])
			bsObject = browser.source()
			image_link = image_get(bsObject)
			price = "'" + str(random.randint(1,301) / 100)
			new_d['MSRP'] = price
			new_d['Product Id'] = self.f_contents[i]['Product Id']
			#new_d['item_name'] = self.f_contents[i][name_d] + ' - ' + self.f_contents[i].get('Finish', 'Regular')
			new_d['Product Image'] = image_link
			#new_d['bullet_point1'] = '1x ' + self.f_contents[i][name_d]
			#new_d['bullet_point2'] = 'This card has a ' + self.f_contents[i].get('Finish', 'Regular') + ' finish'
			#new_d['bullet_point3'] = 'Rarity: ' + self.f_contents[i]['Rarity']
			new_d['Description'] = 'A single individual card from the' + self.params.get('TCG', def_tcg) + ' trading and collectible card game (TCG/CCG). This is of the ' + self.f_contents[i]['Rarity'] + ' rarity.'
			results.append(new_d)
		#results = self.barcode_grab(results)
		new_csv(results)
		self.last_info = results
		return results

	def barcode_grab(self, x):
		for i in range(0, len(x)):
			for i_2 in range(len(self.barcodes), -1, -1):
				#negative loop that removes each barcode it copies over
				x[i]["external_product_id_type"] = "'" + self.barcodes.pop([i_2])
		w_csv(self.barcodes, "Remaining BCs.csv")
		return x



def new_csv(x, output='test.csv'):
	columns = [list(x[0].keys())]
	keys = list(x[0].keys())
	for i in range(0, len(x)):
		new_item = []
		for i_2 in range(0, len(keys)):
			new_value = x[i][keys[i_2]]
			new_item.append(new_value)
		columns.append(new_item)
	w_csv(columns, output)
	return columns




def image_get(x):
	bsObject = x
	items = bsObject.find('div', {'class':'span4'})
	rows = items.find_all('li')
	image_link_element = rows[0].find('a',{'class':'thumbnail'})
	image_link = 'https:' + S_format(str(image_link_element)).linkf('href=').split('?')[0]
	return image_link
#testing image_get function
def t_image_get(x):
	browser.prod_go_to(x)
	test = image_get(browser.source())
	return test
def t_new_csv(x):
	test_d = dictionarify(x)
	test = new_csv(test_d)
	return test
def t_main(x):
	test_obj = Main(x)
	results = test_obj.g_info()
	return results
