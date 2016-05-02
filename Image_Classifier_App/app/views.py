import os
import numpy as np
from PIL import Image, ImageStat
from sklearn.svm import SVC
from cPickle import load
from urllib import unquote

from django.shortcuts import render, redirect
from django.http import HttpResponse
from app.models import Picture, Classifier

def index(request):
	return render(request, 'index.html')

def classifier(request, classifier_name):
	classifier = Classifier.objects.get(name=classifier_name)
	if request.method == 'GET':
		context = { 'name': classifier.name, 'class0': classifier.class0,
					'class1': classifier.class1, 'algorithm': classifier.algorithm,
					'description': classifier.description }
		return render(request, 'classifier.html', context)
	else:
		pictureFiles = request.FILES.getlist('img')
		print pictureFiles
		newPicsList = []
		for pic in pictureFiles:
			newPic = Picture(picture = pic)
			newPic.save()
			newPicsList.append(newPic)
		return classificationResult(request, classifier, newPicsList)

def classificationResult(request, classifier, imageList):
	BASE_DIR = os.path.dirname(os.path.dirname(__file__))
	MEDIA_DIR = BASE_DIR + '/media/'
	pickledClassifierPath = (BASE_DIR + '/featured_classifiers/' + 
		classifier.name + '/' + classifier.name + 'Classifier.pkl')
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
		imageFeaturesArray = np.array([int(float(imageFeatures['rMean'])), 
			int(float(imageFeatures['gMean'])), int(float(imageFeatures['bMean'])),
			int(float(imageFeatures['rStdDev'])), int(float(imageFeatures['gStdDev'])), 
			int(float(imageFeatures['bStdDev']))])
		prediction = clf.predict(imageFeaturesArray)
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
	return imageFeatures

def instagramRequest(request):
	if request.method == 'GET':
		return redirect('https://api.instagram.com/oauth/authorize/?client_id=23baa096a76d4bc6b97d72cfc3e916ad&redirect_uri=http://localhost:8000/redirect/&response_type=code')
		#return render(request, 'addClassifier.html')
	else:
		pass

def addClassifier(request):
	if request.method == 'GET':
		code = request.GET['code']
		authURL = 'https://api.instagram.com/oauth/access_token'
		data = {
			'client_id': '23baa096a76d4bc6b97d72cfc3e916ad',
			'client_secret': '73a1c78e62f54b4798bbf99d590f8d50',
			'grant_type': 'authorization_code',
			'redirect_uri': 'http://localhost:8000/redirect/',
			'code': code
		}
		r = requests.post(authURL, data=data)
		access_token = json.loads(r.text)['access_token']
		context = { 'access_token': access_token}
		return render(request, 'addClassifier.html', context)
	else:
		pass
