import feature as f
import numpy as np
import math

# binary ID3

class id3:

	def __init__(self,training, k = 1):
		self.train_data    = []
		self.train_class   = []
		self.mean = [0,0,0]
		self.k = k

		for i in range(len(training)):
			d = training[i]
			f1,f2,f3 = self.getFeature(d.data_list)
			self.train_data.append([f1,f2,f3])
			self.train_class.append(int(d.label))

		for i in range(3):
				f_sum = 0.0
				for d in self.train_data:
					f_sum += d[i]
				self.mean[i] = f_sum / len(self.train_data)

		#print self.mean
		for d in self.train_data:
			self.adjustFeature(d)
		#print self.train_data
		#print self.train_class

		#print self.calc_info_gain(self.train_data,self.train_class,0)
		#print self.calc_info_gain(self.train_data,self.train_class,1)
		#print self.calc_info_gain(self.train_data,self.train_class,2)

		self.tree = self.make_tree(self.train_data,self.train_class,['f1','f2','f3'])
		#self.printTree(self.tree,'')

	def getFeature(self,data_list):
		f1 = f.max_sys(data_list)  #
		f2 = f.min_sys(data_list)  
		f3 = f.calc_sys_dia_var(data_list)
		return f1,f2,f3

	def calc_entropy(self,p):
		if p != 0:
			return - p * math.log(p,2)
		return 0

	def calc_info_gain(self,data,classes,feature):

		# Calculates the information gain based on both entropy and the Gini impurity
		gain = 0
		nData = len(data)

		# List the values that feature can take

		values = []
		for datapoint in data:
			if datapoint[feature] not in values:
				values.append(datapoint[feature])
		#print values
		featureCounts = np.zeros(len(values))
		entropy = np.zeros(len(values))
		valueIndex = 0
		# Find where those values appear in data[feature] and the corresponding class
		for value in values:
			dataIndex = 0
			newClasses = []
			for datapoint in data:
				if datapoint[feature]==value:
					featureCounts[valueIndex]+=1
					newClasses.append(classes[dataIndex])
				dataIndex += 1

			# Get the values in newClasses
			classValues = []
			for aclass in newClasses:
				if classValues.count(aclass)==0:
					classValues.append(aclass)

			classCounts = np.zeros(len(classValues))
			classIndex = 0
			for classValue in classValues:
				for aclass in newClasses:
					if aclass == classValue:
						classCounts[classIndex]+=1 
				classIndex += 1
			
			for classIndex in range(len(classValues)):
				entropy[valueIndex] += self.calc_entropy(float(classCounts[classIndex])/np.sum(classCounts))

			# Computes both the Gini gain and the entropy
			gain = gain + float(featureCounts[valueIndex])/nData * entropy[valueIndex]
			valueIndex += 1
		return gain
			


	def classify(self,tree,datapoint,featureNames):
		if type(tree) == type(123):
			# Have reached a leaf
			return tree
		else:
			a = tree.keys()[0]
			for i in range(len(featureNames)):
				if featureNames[i]==a:
					break
			#print a,i,datapoint[i],tree[a][datapoint[i]]
			try:
				t = tree[a][datapoint[i]]
				return self.classify(t,datapoint,featureNames)
			except:
				return None

	def printTree(self,tree,name):
			if type(tree) == dict:
				print name, tree.keys()[0]
				for item in tree.values()[0].keys():
					print name, item
					self.printTree(tree.values()[0][item], name + "\t")
			else:
				print name, "\t->\t", tree

	def make_tree(self,data,classes, featureNames,maxlevel=-1,level=0,forest=0):
		""" The main function, which recursively constructs the tree"""

		nData = len(data)
		nFeatures = len(data[0])

		# List the possible classes
		newClasses = []
		for aclass in classes:
			if newClasses.count(aclass) == 0:
				newClasses.append(aclass)

		# Compute the default class (and total entropy)
		frequency = np.zeros(len(newClasses))

		totalEntropy = 0
		index = 0
		for aclass in newClasses:
			frequency[index] = classes.count(aclass)
			totalEntropy += self.calc_entropy(float(frequency[index])/nData)
			index += 1

		default = classes[np.argmax(frequency)]

		if nData==0 or nFeatures == 0 or (maxlevel>=0 and level>maxlevel):
			# Have reached an empty branch
			return default
		elif classes.count(classes[0]) == nData:
			# Only 1 class remains
			return classes[0]
		else:
			# Choose which feature is best	
			gain = np.zeros(nFeatures)
			featureSet = range(nFeatures)
			if forest != 0:
				np.random.shuffle(featureSet)
				featureSet = featureSet[0:forest]
			for feature in featureSet:
				g = self.calc_info_gain(data,classes,feature)
				gain[feature] = totalEntropy - g
			bestFeature = np.argmax(gain)
			tree = {featureNames[bestFeature]:{}}

			# List the values that bestFeature can take
			values = []
			for datapoint in data:
				if datapoint[feature] not in values:
					values.append(datapoint[bestFeature])

			for value in values:
				# Find the datapoints with each feature value
				newData = []
				newClasses = []
				index = 0
				for datapoint in data:
					if datapoint[bestFeature]==value:
						if bestFeature==0:
							newdatapoint = datapoint[1:]
							newNames = featureNames[1:]
						elif bestFeature==nFeatures:
							newdatapoint = datapoint[:-1]
							newNames = featureNames[:-1]
						else:
							newdatapoint = datapoint[:bestFeature]
							newdatapoint.extend(datapoint[bestFeature+1:])
							newNames = featureNames[:bestFeature]
							newNames.extend(featureNames[bestFeature+1:])
						newData.append(newdatapoint)
						newClasses.append(classes[index])
					index += 1
				# print '------------------------------'
				# print newData
				# print newClasses
				# print newNames
				# Now recurse to the next level	
				subtree = self.make_tree(newData,newClasses,newNames,maxlevel,level+1,forest)

				# And on returning, add the subtree on to the tree
				tree[featureNames[bestFeature]][value] = subtree

			return tree


	def adjustFeature(self,d):
		for i in range(3):
			if d[i] <= self.mean[i] * self.k:
				d[i] = 0
			else:
				d[i] = 1

	def testID3(self,testing):
			datapoint = list(self.getFeature(testing))
			self.adjustFeature(datapoint)
			res = self.classify(self.tree,datapoint,['f1','f2','f3'])
			return str(res)