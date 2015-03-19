import pylab
import random
import nn
import knn
res = []
data = []
labels = []


# How to use
def ml(d,l):
	for ele in d:
		data.append(ele)
	for ele in l:
		labels.append(ele)
	res = []
	for i in range(10):
		run_ml()
	output()
	drawROC()

def run_ml(k = 1):
	total = len(data)
	num_test = int(total * 0.3)

	train_data = []
	train_labels = []
	test_data  = []
	test_labels = []

	train_data   = data[:]
	train_labels = labels[:]

	n = total
	for i in range(num_test):
		index = int(random.random() * n)
		n -= 1
		test_data.append(train_data.pop(index))
		test_labels.append(train_labels.pop(index))
	# train
	import nn
	classifier_nn = nn.nn(train_data,train_labels)
	import knn
	classifier_knn = knn.knn(train_data,train_labels)
	# test
	for i in range(len(test_data)):
		d = test_data[i]
		res.append([classifier_nn.test(d), classifier_knn.test(d,k), test_labels[i]])

def train(d, l, w, th):
	classifier_nn = nn.nn(d,l,w,th)
	classifier_knn = knn.knn(d,l)
	return classifier_nn, classifier_knn


def output():
	for classifier in range(2):
		if classifier == 0:
			print "-------------------NN-----------------"
		else:
			print "------------------kNN-----------------"
		print "Confusion Matrix:", cal_tp_fp_fn_tn(classifier)
		print "Accuracy:", getAccuracy(classifier)
		print "Sensitivity", getSensitivity(classifier)
		print "Specificity", getSpecificity(classifier)
		print "Precision", getPrecision(classifier)
		print "Recall", getRecall(classifier)
		print "F Measurement", getFmeasurement(classifier)

def cal_tp_fp_fn_tn(classifier):
	tp, fp, fn, tn = 0, 0, 0, 0
	for x in res:
		if x[-1] == 0:
			if x[classifier] == x[-1]:
				tn += 1
			else:
				fn += 1
		else:
			if x[classifier] == x[-1]:
				tp += 1
			else:
				fp += 1
	return tp, fp, fn, tn

def getAccuracy(classifier):
	tp, fp, fn, tn = cal_tp_fp_fn_tn(classifier)
	return (tp + tn)*1.0/(tp+fp+fn+tn)

def getSensitivity(classifier):
	tp, fp, fn, tn = cal_tp_fp_fn_tn(classifier)
	if tp + fn > 0:
		return (tp)*1.0/(tp+fn)
	return -1

def getSpecificity(classifier):
	tp, fp, fn, tn = cal_tp_fp_fn_tn(classifier)
	if fp + tn > 0:
		return (tn)*1.0/(fp+tn)
	return -1

def getPrecision(classifier):
	tp, fp, fn, tn = cal_tp_fp_fn_tn(classifier)
	if tp + fp > 0:
		return (tp)*1.0/(tp+fp)
	return -1

def getRecall(classifier):
	tp, fp, fn, tn = cal_tp_fp_fn_tn(classifier)
	if tp + fn > 0:
		return (tp)*1.0/(tp+fn)
	return -1

def getFmeasurement(classifier):
	tp, fp, fn, tn = cal_tp_fp_fn_tn(classifier)
	if tp + fn + fp > 0:
		return (tp)*1.0/(tp+(fn+fp)/2.0)
	return -1

def getROCPoints(classifier):
	points = [[0,0],[1,1]]
	tmp = []
	if classifier == 0: # NN
		while (len(points) < 100):
			res = []
			run_ml()
			tp, fp, fn, tn = cal_tp_fp_fn_tn(classifier)
			if tp+fn > 0 and fp+tn>0:
				y = tp * 1.0 / (tp+fn)
				x = fp * 1.0 / (fp+tn)
				points.append([x,y])
	else:
		for k in range(15):
			res = []
			run_ml(k+1)
			tp, fp, fn, tn = cal_tp_fp_fn_tn(classifier)
			if tp+fn > 0 and fp+tn>0:
				y = tp * 1.0 / (tp+fn)
				x = fp * 1.0 / (fp+tn)
				points.append([x,y])

	points.sort()
	lx = [int(p[0]*100) for p in points]
	ly = [int(p[1]*100) for p in points]
	return lx,ly

def drawROC():
	pylab.figure()
	pylab.xlabel('False Positive Rate(%)')
	pylab.ylabel('True  Positive Rate(%)')
	pylab.title('ROC Curve')

	# draw NN
	x,y = getROCPoints(0)
	pylab.plot(x,y, c='red', label = "NN")

	# draw kNN
	x,y = getROCPoints(1)
	pylab.plot(x,y, c='blue', label = "kNN")

	pylab.legend()
	pylab.show()


# training = [[1,1],[1,-1],[-1,1],[-1,-1],[-1,1],[2,3],[0,1],[-2,3],[3,4],[8,9]]
# labels   = [1,1,0,0,1,1,0,1,0,1]

f   = open('./local_detection/data.txt', 'r')
train_data   = []
train_labels = []
w = [-195810.7621348925, 68488.99265190709, -38897.842134328814, 68488.7823538183, 13755.655375035134]
th = 813.652987128

for line in f:
	d = []
	for u in line.split():
		d.append(int(float(u)))
	train_labels.append(d.pop())
	train_data.append(d[:])
classifier_nn, classifier_knn = train(train_data,train_labels,w,th)

def test(d,nn=classifier_nn,knn=classifier_knn):
	return nn.test(d), knn.test(d)
