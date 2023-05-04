import time

dict = {}
list = []

for i in range(0,100):
	x = i
	dict[0] = x
	dict[1] = x+1
	list.append(dict)
	dict = {}

print(list)

time.sleep(10)