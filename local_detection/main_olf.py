from detect_olf import det
import sys, select, os
import threading
import time
import test_olf as t

def run():
    global pos
    global n_time
    #print "start point: ", pos, n_time
    pos, data,labels = det(pos,n_time)
    #print "pos:",pos
    #print "data: ",data
    #print "labels:",labels
    n_time += 1
    rnn, rknn = t.test(data[0])
    print "-------------------------------------------------------"
    if rnn  == 1 and rknn == 1:
        print "Both NN and kNN detect a DDoS"
    elif rknn == 1:
        print "kNN detects a DDoS"
    elif rnn == 1:
        print "NN detects a DDoS"
    else:
        print "No DDoS!"
    print "-------------------------------------------------------"
pos = 0
n_time = 1
