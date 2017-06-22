from dbaseObject import *
from text_l import *
from w_csv import *
import sys
#grabs list of products added to preorder data base before the current date

def item_adds(month, day, year = "2017"):
	text_cred = text_l('C:\\Users\\Owner\\Documents\\Important\\catcred.txt')
	dbObject = Db_mngmnt(text_cred[2],text_cred[3],'preorders', '192.168.5.90')
	res = dbObject.query(
			"SELECT product_name, product_id FROM preorders.adds WHERE date_added > \"{0}-{1}-{2} 00:00:00\"".format(
						year, dbObject.leading_zero(str(month), 2), dbObject.leading_zero(str(day), 2)))
	return res

if __name__ == "__main__":
	res = item_adds(sys.argv[1], sys.argv[2])
	w_csv(res)
