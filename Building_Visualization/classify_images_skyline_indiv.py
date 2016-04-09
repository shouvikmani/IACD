import os
import shutil
import csv
import json
import sys
import numpy as np
from sklearn.svm import SVC

def classifyImages(buildingName, clf):
	buildingPath = 'data/' + buildingName
	buildingImages = os.listdir(buildingPath)
	os.mkdir(buildingPath + '/skylineClassified/')
	os.mkdir(buildingPath + '/individualClassified/')
	for img in buildingImages:
		imageFilePath = buildingPath + '/' + img
		metadataFilePath = buildingPath + '/meta' + img[:-4] + '.json'
		try:
			metadata = json.loads(readData(metadataFilePath))
		except:
			continue
		imageFeatures = np.array([int(float(metadata['features']['rMean'])), 
			int(float(metadata['features']['gMean'])), int(float(metadata['features']['bMean'])),
			int(float(metadata['features']['rStdDev'])), int(float(metadata['features']['gStdDev'])), 
			int(float(metadata['features']['bStdDev']))])
		prediction = clf.predict(imageFeatures)
		if prediction == 1:
			os.symlink(os.getcwd() + '/' + imageFilePath, buildingPath + '/individualClassified/' + img)
		else:
			os.symlink(os.getcwd() + '/' + imageFilePath, buildingPath + '/skylineClassified/' + img)

def formatLabels(trainingData):
	completeLabels = []
	for d in trainingData:
		if d['skyline/individual'] == 'individual':
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

def readData(source):
	with open(source, 'r') as f:
		content = f.read()
	return content

def readCSVData(source):
	with open(source) as csvfile:
		reader = csv.DictReader(csvfile)
		content = []
		for row in reader:
			content.append(row)
	return content

def main():
	buildingName = sys.argv[1]
	trainingData = readCSVData('training_data/skylineIndividual.csv')
	features = formatFeatures(trainingData)
	labels = formatLabels(trainingData)
	clf = SVC(kernel='linear')
	clf.fit(features, labels)
	classifyImages(buildingName, clf)

if __name__ == '__main__':
	main()
