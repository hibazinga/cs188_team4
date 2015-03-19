from detect_olf import det
import sys, select, os
import threading
import time
import test_olf as t

def run():
    global pos
    global n_time
    print "start point: ", pos, n_time
    pos, data,labels = det(pos,n_time)
    print "pos:",pos
    print "data: ",data
    print "labels:",labels
    n_time += 1
    rnn, rknn = t.test(data[0])
    if rnn  == 1:
        print "NN detects a DDOS"
    if rknn == 1:
        print "KNN detects a DDOS"


pos = 0
n_time = 1
