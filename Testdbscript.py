import re
from soupclass8 import C_sort,r_csv
import csv
import mysql.connector
import time
from dictionarify import dictionarify
from text_l import text_l
from dbaseObject import *


class TestdbScript:
    def __init__(self, credFile = 'C:\\Users\\Owner\\Documents\\Important\\catcred.txt', host = '192.168.5.90', credFile2 = 'C:\\Users\\Owner\\Documents\\Important\\cat_cred2.txt',*args):
        self.text_cred = text_l(credFile)
        self.dbObject = Db_mngmnt(self.text_cred[2], self.text_cred[3],'cc_def_products', '192.168.5.90')
    def dbase_q_form(self, x):
        #used to prepare values before they are entered into a sql database
        data = x
        data = data.replace('"', '\\"')
        data = data.replace("'", "\\'")
        data = data.replace("\\",'')
        return data

    def addCSV(self, doc):
        data = dictionarify(doc)
        for item in data:
            for i in list(item.keys()):
                item[i] = self.dbase_q_form(item[i])
                if not item["Barcode"]:
                    item["Barcode"] = "NULL"

        for item in data:
            print("Adding {0}".format(item["Product Name"]))
            command = """INSERT INTO products (name, barcode, date_added, cc_id, aspect, cc_genre, release_date, sound, studio, versions, year)
                VALUES (\"{0}\", {1}, \"{2}\", {3}, \"{4}\", \"{5}\", \"{6}\", \"{7}\", \"{8}\", \"{9}\", \"{10}\")""".format(
                    item['Product Name'], item['Barcode'], self.dbObject.date_form(), item['Product Id'],
                    item['Aspect'], item['Genre'], item['Release Date'], item['Sound'], item['Studio'], item['Versions'], item['Year'])
            print(command)
            self.dbObject.cust_com(command)
test = TestdbScript()
