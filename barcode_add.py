#barcode addition program
from dbaseObject import *
from text_l import *
import sys

def add(bcodes_file):
	text_cred = text_l('C:\\Users\\Owner\\Documents\\Important\\catcred.txt')
	dbObject = Db_mngmnt(text_cred[2],text_cred[3],'asins', '192.168.5.90')
	bcs = text_l(bcodes_file)
	for i in bcs:
		if str(i).isdigit():
			dbObject.cust_com("INSERT INTO asins.barcodes (barcode, date_added) VALUES (\"{0}\", \"{1}\");".format(str(i), dbObject.date_form()))
	return "Added {0} barcodes".format(len(bcs))



if __name__ == "__main__":
	add(sys.argv[1])