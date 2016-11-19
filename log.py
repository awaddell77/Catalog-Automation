#log file 

import time
def main(x):
	date = x
	data = ''
	end = ['Exit', 'exit', 'quit', 'q', 'Logout','Log off']
	while data not in end:
		data = input('Log Input:')
		command = ['?']
		'''if 'data in none_list':
			if data[0] == '?':
				print('Do something.')'''
		if data != '':
			entry_maker([data])#needs to be list
			entry_maker([data], "C:\\Users\\Owner\\Documents\\LOG BACKUP\\logfile_backup.txt")

def entry_maker(x,fname='C:\\Users\\Owner\\logfile.txt'):
	with open(fname, 'a') as f:
		for i in range(0, len(x)):
			date = " (%d - %d - %d)" % (time.localtime()[1], time.localtime()[2], time.localtime()[0])
			f.writelines(x[i] + date + "\n") 
	#should add date and time to this 
	#note that on non-windows systems the file mode may need to be changed since "a" automatically treats the file as a binary
	print("%s has been added to logfile." % (x))