import time

def bar(total):
	print("PROGRESS:", end='')
	#time.sleep(10)
	inc = total // 10
	n = 0
	d_queue = []
	while True:
		d_queue.append('1')
		n += 1
		#print(n)
		if n == inc:
			print("#", end='', flush = True)
			n = 0
			time.sleep(1)
		elif len(d_queue) >= total:
			time.sleep(.5)
			print('#', flush = True)
			break


		