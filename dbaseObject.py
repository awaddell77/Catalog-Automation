#mysql 
import re
from soupclass8 import C_sort,r_csv
import csv
import mysql.connector

print("mysql.connector.connect(user='username', password='passsword', host='127.0.0.1', database='database_name'")
class Db_mngmnt(object):
	def __init__(self, user, password, database, host):
		self.user = user 
		self.password = password
		self.database = database
		self.host = host
		self.con = mysql.connector.connect(user=self.user, password=self.password, host=self.host, database=self.database)
		self.cursor = self.con.cursor(buffered = True)
		self.last_resp = ''
	
	def reconnect(self):
		self.con = mysql.connector.connect(user=self.user, password=self.password, host=self.host, database=self.database)
		self.cursor = self.con.cursor(buffered = True)
		#return cursor

	def import_data(self, fname):
		info = C_sort(fname)
		db_columns = info.row(0)
		db_contents = info.contents[1:]
		return db_columns, db_contents

	def table_create(self, x, table_name, location=''):
		#creates table of text columns usings the provided list as column headers
		new = [re.sub(' ', '_', x[i].strip(' ')) + " TEXT" for i in range(0, len(x))]
		contents = ', '.join(new)
		if location == '':
			return 'CREATE TABLE ' + table_name + ' (' + contents + ') ;'
		else:
			return 'CREATE TABLE ' + table_name +'.'+ location + ' (' + contents + ') ;'
	def table_data_prep(self, x):
		for i in range(0, len(x)):
		#adds quotes to every item on a csv list
			for i_2 in range(0, len(x[i])):
				x[i][i_2] = '"' + x[i][i_2] + '"'
		return x 
	def table_insert(self, x, table):
		results = []
		x = table_data_prep(x)
		for i in range(0, len(x)):
			values = '(' + ', '.join(x[i]) + ') ;'
			command = 'INSERT INTO %s VALUES %s' % (table, values)
		#print(command)
			results.append(command)
		return results
	def row_insert_single_batch(self, table_name, x, database=''):
		for i in range(0, len(x)):
			command = self.row_insert_single(table_name, x[i], database)
			"Inserting \" {0} \" now.".format(command)
			self.cursor.execute(command)
		self.con.commit()
		return

	def row_insert_single(self, table_name, x, database = ''):
		values = ['"' + string_cleanse(str(x[i])) + '"' for i in range(0, len(x))]
		if database == '':
			command = "INSERT INTO {0} VALUES ({1})".format(table_name, ", ".join(values))
		else:
			command = "INSERT INTO {0}.{1} VALUES ({2})".format(database, table_name, ", ".join(values))
		return command
	def batch_row_insert_main(self, table_name, x, columns, database = ''):
		values = []
		for i in range(0, len(x)):
			values.append(self.batch_row_insert_form(x[i]))
		columns =  [re.sub(' ', '_', columns[i]) for i in range(0, len(columns))]


		if database == '':
			command = "INSERT INTO {0} ({1}) VALUES {2}".format(table_name,", ".join(columns), ", ".join(values))
		else:
			command = "INSERT INTO {0}.{1} ({2}) VALUES {3}".format(database, table_name, ", ".join(columns), ", ".join(values))
		self.cursor.execute(command)
		self.con.commit()
		return command

	def batch_row_insert_form(self, x):
		values_r = ['"' + str(x[i]) + '"' for i in range(0, len(x))]
		values = "({0})".format(", ".join(values_r))
		return values
	def query(self, x):
		self.cursor.execute(x)
		rows = self.cursor.fetchall()
		self.last_resp = rows
		return rows
	def query_multi(self, x):
		self.cursor.execute(x, multi=True)
		rows = self.cursor.fetchall()
		self.last_resp = rows
		return rows
	def __comm(self, command, query = 0):
		#does not add response to last_resp data field
		self.cursor.execute(x)
		if query == 0:
			self.con.commit
		else:
			rows = self.cursor.fetchall()
			return rows
	def cust_com(self, x):
		self.cursor.execute(x)
		self.con.commit()
	def copy_row(self, x):
		pass
	def retr_columns(self, table, dtypes = 0):
		#retrieves the column names, returns them in a list
		#if dtypes is not 0 then it returns them in a list of tuples (column name, data type)

		resp = self.query("SHOW COLUMNS from {0};".format(table))
		if dtypes == 0:
			columns = [i[0] for i in resp]
			return columns
		else:
			results = []
			for i in resp:
				results.append((i[0], i[1]))
			return results
	def tables(self):
		resp = self.__comm("SHOW tables;", 1)
		tables = [i[0] for i in resp]
		return tables

	def date_form(self):
	    #returns the current date in the YYYY-MM-DD HH:MM:SS required by the datetime data type in mysql
	    full_dt = time.localtime()
	    year = str(full_dt[0])
	    month = self.leading_zero(full_dt[1],2)
	    day = self.leading_zero(full_dt[2], 2)
	    hour = self.leading_zero(full_dt[3],2)
	    minutes = self.leading_zero(full_dt[4], 2)
	    seconds = self.leading_zero(full_dt[5],2)
	    date_time = "{0}-{1}-{2} {3}:{4}:{5}".format(year, month, day, hour, minutes, seconds)
	    return date_time
	def leading_zero(self, x, length):
	    if len(str(x)) < length:
	        return "0" + str(x)
	    else:
	        return str(x)

def string_cleanse(x):
	new = re.sub('"', '', x)
	new2 = re.sub("'", '', new)
	return new2

'''
def login(user, password, database = '', host= '127.0.0.1'):
	cnx = mysql.connector.connect(user=user, password=password, host=host)
	#cursor = cnx.cursor(buffered = True)
	return cnx
'''





test_list = ['test1','test2', 'test3', 'test4' , 'test5']
test_list2 = [['test1','test2', 'test3', 'test4' , 'test5'], ['test1','test2', 'test3', 'test4' , 'test5'], 
['test1','test2', 'test3', 'test4' , 'test5'], ['test1','test2', 'test3', 'test4' , 'test5']]

'''test = Db_mngmnt('test','test','test')
print("Testing batch_row_insert_form method")
test.batch_row_insert_form(test_list)
print("Testing batch_row_insert_main")
test.batch_row_insert_main("test", test_list2)'''

