import csv
import numpy as np
from sklearn.svm import SVC
from cPickle import dump

def saveClassifierToFile(clf, target):
	with open(target, 'wb') as f:
		dump(clf, f)

def fitSVMClassifier(features, labels):
	clf = SVC(kernel='linear')
	clf.fit(features, labels)
	return clf

def formatLabels(trainingData):
	completeLabels = []
	for d in trainingData:
		if d['apple/orange'] == 'orange':
			completeLabels.append(1)
		else:
			completeLabels.append(0)
	completeLabels = np.array(completeLabels)
	return completeLabels

def formatFeatures(trainingData):
	completeFeatures = []
	for d in trainingData:
		features = [int(float(d['rMean'])), int(float(d['gMean'])), int(float(d['bMean'])),
					int(float(d['rStdDev'])), int(float(d['gStdDev'])), int(float(d['bStdDev']))]
		completeFeatures.append(features)
	completeFeatures = np.array(completeFeatures)
	return completeFeatures

def readCSVData(source):
	with open(source) as csvfile:
		reader = csv.DictReader(csvfile)
		content = []
		for row in reader:
			content.append(row)
	return content

def main():
	trainingData = readCSVData('appleOrange.csv')
	features = formatFeatures(trainingData)
	labels = formatLabels(trainingData)
	clf = fitSVMClassifier(features, labels)
	saveClassifierToFile(clf, 'appleOrangeClassifier.pkl')

if __name__ == '__main__':
	main()
