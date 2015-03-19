import random

class nn:
	lambd = 0.2
	num_of_loop = 100

	def __init__(self, training, labels, w = [],th = 0):
		if len(w) == 0:
			self.train_data = training
			self.labels = labels
			self.featureNum = len(training[0])
			self.threshold = random.random()
			self.w = [0] * self.featureNum
			self.initWeight()
			self.train()
		else:
			self.w = w
			self.featureNum = len(w)
			self.threshold = th

	def initWeight(self):
		for i in range(self.featureNum):
			self.w[i] = random.random()
			if random.random() < 0.5:
				self.w[i] = - self.w[i]

	def train(self):
		for l in range(self.num_of_loop):
			for d in range(len(self.train_data)):
				data  = self.train_data[d]
				label = self.labels[d] 
				y = self.classify(data)
				
				for i in range(self.featureNum):
			 		self.w[i] -= self.lambd * (y - label) * data[i]
				self.threshold += self.lambd * (y - label)
	
	def classify(self, data):
		y = 0
		for i in range(self.featureNum):
			y += self.w[i] * data[i]
		if y > self.threshold:
			return 1
		else:
			return 0

	def test(self,data_list):
		return self.classify(data_list)

