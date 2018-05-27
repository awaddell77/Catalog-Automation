#video game script
from Cat_dbase import *
from dictionarify import *
import sys
def main():
    catObj = Cat_dbase()
    products = catObj.query("SELECT id FROM products WHERE product_type_id = \"229\" AND barcode IS NOT NULL AND asin IS NOT NULL;")
    for i in range(0, len(products)):
        print("Processing {0} ({1} of {1})".format(products[i][0], i+1, len(products)))
        catObj.update_product(products[i][0], "barcode", "null")
        catObj.update_product(products[i][0], "asin", "null")
def update_by_id(x):
    catObj = Cat_dbase()
    load = "Loading"
    info = dictionarify(x)
    data = catObj.query("SELECT product_id, descriptor_id, value FROM product_descriptors WHERE descriptor_id = \"4971\";")
    print("Loading", end='', flush=True)
    for i in range(0, len(info)):
        info[i]["Product Id"] = ""
        for elements in data:
            print(".", end="", flush= True)
            if info[i]["PCID"] == elements[2]:
                #print("Found {0}".format(info[i]["Product Name"]))
                info[i]["Product Id"] = elements[0]

        #print("Processing {0} ({1} of {2})".format(info[i]["Product Name"], i+1, len(info)))
        #p_id = catObj.query("SELECT product_id FROM product_descriptors WHERE descriptor_id = \"4971\" AND value = \"{0}\";".format(info[i]["PCID"]))
        #info[i]["Product Id"] = p_id[0]


    for i in range(0, len(info)):
        print("Processing {0} ({1} of {2})".format(info[i]["Product Id"], i+1, len(info)))
        if info[i]["Barcode / UPC"] and info[i]["Product Id"]:
            try:
                catObj.update_product(info[i]["Product Id"], "barcode", info[i]["Barcode / UPC"])
            except:
                print("Skipping {0}".format(info[i]["Product Id"]))
                continue
    for i in range(0, len(info)):
        print("Processing {0} ({1} of {2})".format(info[i]["Product Id"], i+1, len(info)))
        if info[i]["ASIN"] and info[i]["Product Id"]:
            try:
                catObj.update_product(info[i]["Product Id"], "asin", info[i]["ASIN"])
            except:
                print("Skipping {0}".format(info[i]["Product Id"]))
                continue






if __name__ == "__main__":
    update_by_id(sys.argv[1])
