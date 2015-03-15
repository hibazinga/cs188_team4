from detect import det
import sys, select, os
import threading
import time


'''
def startDetect(n_time,last_pos):
  threading.Timer(exe_interval,startDetect,[n_time,last_pos]).start()
  #execute local detection on part of the file
  last_pos[0] = det(last_pos[0], n_time[0])
  n_time[0] += 1

startDetect(n_time,last_pos) 
'''



def run_ml(data, labels):
	total = len(data)
	num_train = int(total * 0.7)

	train_data = []
	train_labels = []
	test_data  = []
	test_labels = []

	for i in range(num_train):
		train_data.append(data[i])
		train_labels.append(labels[i])

	for i in range(num_train,total):
	  	test_data.append(data[i])
	  	test_labels.append(labels[i])

	import nn
	classifier_nn = nn.nn(train_data,train_labels)
	correct = 0
	for i in range(len(test_data)):
		res = classifier_nn.test(test_data[i])
		if res == test_labels[i]:
			correct += 1
	print "nn:", correct * 1.0 / len(test_data)

	import knn
	classifier_knn = knn.knn(train_data,train_labels)
	correct = 0
	for i in range(len(test_data)):
		res = classifier_knn.test(test_data[i],5)
		if res == test_labels[i]:
			correct += 1
	print "knn:", correct * 1.0 / len(test_data)

    
pos, data,labels = det(0,1)
run_ml(data,labels)
'''
#press enter to stop the process
exe_interval = 20
last_pos = 0
n_time = 1

while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    print "Press Enter to stop me!"
    #process to be called
    
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        line = raw_input()
        break
    temp_res = det(last_pos,n_time)
    last_pos = temp_res[0]
    result = temp_res[1]
    print result
    
    n_time = n_time + 1
    time.sleep(3)
'''