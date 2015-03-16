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


pos, data,labels = det(0,1)
fdata   = open('data.txt', 'w')

num = len(data)
for i in range(num):
    d = data[i]
    l = labels[i]
    for ele in d:
      fdata.write(str(ele))
      fdata.write(' ')
    fdata.write(str(l))
    fdata.write('\n')

fdata.close()
# test.ml(data, labels)
import test

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
    for d in result:
        test.test(d)
    n_time = n_time + 1
    time.sleep(30)

'''