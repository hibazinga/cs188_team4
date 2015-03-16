import sys
import pylab
import random
import numpy

def main():
    file = open("label","r")
    line=file.readline()
    x=line.split(', ') #label
    line=file.readline()
    y=line.split(', ') #nn
    line=file.readline()
    z=line.split(', ') #knn
    print len(x)
    print len(y)
    print len(z)
    file.close()
    file = open("predict","r")
    line=file.readline()
    b=[]
    while line:
        b.append(line)
        line=file.readline()
    print len(b)
    file.close()
    tp=0
    tn=0
    fp=0
    fn=0
    for i in range(0,len(x)):
        real=int(x[i][0])
        pred=int(b[i][0])
        if real==1 and pred==1:
            tp+=1
        elif real==1 and pred==0:
            tn+=1
        elif real==0 and pred==1:
            fp+=1
        elif real==0 and pred==0:
            fn+=1

    print ' tp = ',tp,' tn = ', tn,' fp = ', fp, ' fn = ',fn

    print 'Accuracy = ', (tp+tn)*1.0/len(x)

    print 'Sensitivity = ', (tp) *1.0 /(tp+fn)

    print 'Specificity = ', (tn) *1.0 / (tn+fp)

    print 'Precision = ', (tp)*1.0 / (tp+fp)

    print 'Recall = ', tp*1.0 / (tp+fn)

    print 'F-measure = ', tp*1.0 / (tp+(fn+fp)/2.0)


    axis=[]
    for i in range (0,len(x)):
        axis.append(i)

    for i in range (0,len(x)):
        x[i]=str(int(x[i][0])*2)
    pylab.figure()
    pylab.xlabel('Time (5 sec as an interval)')
    pylab.ylabel('Under Attack')
    pylab.title('Time - Attack Graph')


    # draw attack
    aa=pylab.plot(axis,x, c='black', label = "Actual attack")
	# draw NN
    nn=pylab.plot(axis,y, c='red', label = "NN")

	# draw kNN
    knn=pylab.plot(axis,z, c='green', label = "kNN")

    # draw backscatter
    bs=pylab.plot(axis,b, c='yellow', label = "Backscatter")

    pylab.legend(loc='upper right')

    pylab.show()

main()
