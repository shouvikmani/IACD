import os
import json
import cStringIO
from cPickle import dump
import numpy as np
from PIL import Image, ImageStat
from sklearn.svm import SVC
from cPickle import load
from urllib import unquote, urlopen

from django.shortcuts import render, redirect
from django.http import HttpResponse
from app.models import Picture, Classifier

def index(request):
	classifiers = Classifier.objects.all()
	print classifiers
	context = { 'classifiers': classifiers}
	return render(request, 'index.html', context)

def classifier(request, classifier_name):
	classifier = Classifier.objects.get(name=classifier_name)
	if request.method == 'GET':
		context = { 'name': classifier.name, 'class0': classifier.class0,
					'class1': classifier.class1, 'algorithm': classifier.algorithm,
					'description': classifier.description }
		return render(request, 'classifier.html', context)
	else:
		pictureFiles = request.FILES.getlist('img')
		newPicsList = []
		for pic in pictureFiles:
			newPic = Picture(picture = pic)
			newPic.save()
			newPicsList.append(newPic)
		return classificationResult(request, classifier, newPicsList)

def classificationResult(request, classifier, imageList):
	BASE_DIR = os.path.dirname(os.path.dirname(__file__))
	MEDIA_DIR = BASE_DIR + '/media/'
	pickledClassifierPath = (BASE_DIR + '/classifiers/' + classifier.name + 
							'Classifier.pkl')
	with open(pickledClassifierPath, 'rb') as f:
		clf = load(f)
	imageClassificationDict = {
		classifier.class0: [],
		classifier.class1: []
	}
	for img in imageList:
		picFilePath = MEDIA_DIR + img.picture.url
		picFilePathDecoded = unquote(picFilePath)
		imageFeatures = getImageFeatures(picFilePathDecoded)
		prediction = clf.predict(imageFeatures)
		if prediction == 0:
			imageClassificationDict[classifier.class0].append(img.picture.url)
		else:
			imageClassificationDict[classifier.class1].append(img.picture.url)
	context = { 'imageClassificationDict': imageClassificationDict,
				'class0': classifier.class0, 'class1': classifier.class1 }
	return render(request, 'classificationResults.html', context)

def getImageFeatures(imagePath):
	image = Image.open(imagePath)
	stat = ImageStat.Stat(image)
	pixelMean = stat.mean
	pixelStdDev = stat.stddev
	imageFeatures = {
		'rMean': pixelMean[0],
		'gMean': pixelMean[1],
		'bMean': pixelMean[2],
		'rStdDev': pixelStdDev[0],
		'gStdDev': pixelStdDev[1],
		'bStdDev': pixelStdDev[2]
	}
	imageFeaturesArray =  np.array([int(float(imageFeatures['rMean'])), 
		int(float(imageFeatures['gMean'])), int(float(imageFeatures['bMean'])),
		int(float(imageFeatures['rStdDev'])), int(float(imageFeatures['gStdDev'])), 
		int(float(imageFeatures['bStdDev']))])
	return imageFeaturesArray

def addClassifier(request):
	if request.method == 'GET':
		return render(request, 'addClassifier.html')
	else:
		classifierName = request.POST['classifierName']
		class0 = request.POST['class0']
		class1 = request.POST['class1']
		description = request.POST['description']
		imageClassifications = json.loads(request.POST['imageClassificationsJSON'])
		BASE_DIR = os.path.dirname(os.path.dirname(__file__))
		classifierFilePath = BASE_DIR + '/classifiers/' + classifierName + 'Classifier.pkl'
		trainClassifier(imageClassifications, classifierFilePath)
		newClassifier = Classifier(name=classifierName, class0=class0, class1=class1,
									algorithm="SVM Classifier", description=description,
									isFeatured=False)
		newClassifier.save()
		return redirect(index)

def trainClassifier(imageClassifications, classifierFilePath):
	features = []
	labels = []
	for imageData in imageClassifications:
		try:
			imageURL = imageData['url']
			imageLabel = imageData['label']
			img = cStringIO.StringIO(urlopen(imageURL).read())
			imageFeatures = getImageFeatures(img)
			features.append(imageFeatures)
			labels.append(imageLabel)
		except:
			imageURL = imageData['url']
			print imageURL
			continue
	clf = fitSVMClassifier(np.array(features), np.array(labels))
	saveClassifierToFile(clf, classifierFilePath)
	return

def fitSVMClassifier(features, labels):
	clf = SVC(kernel='linear')
	clf.fit(features, labels)
	return clf

def saveClassifierToFile(clf, target):
	with open(target, 'wb') as f:
		dump(clf, f)
