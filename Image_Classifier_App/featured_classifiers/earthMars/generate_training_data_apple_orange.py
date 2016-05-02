import os
import sys
import random
import json
import csv
import Tkinter
from PIL import Image, ImageTk, ImageStat

class Trainer:
	def __init__(self):
		self.currentFile = ''
		self.currentFileNum = 0
		self.fileName = 'appleOrange.csv'
		self.fieldnames = ['imageFilePath','rMean','gMean','bMean', 
							'rStdDev','gStdDev','bStdDev','apple/orange']

	#Runs GUI that lets user classify images to
	#create labels for training data
	def generateTrainingDataLabels(self, randomImageSample):
		setHeaders(self.fileName, self.fieldnames)
		root = Tkinter.Tk()
		root.bind("<Key>", self.exit_mainloop)
		for file in randomImageSample:
			self.currentFileNum += 1
			try:
				image = Image.open(file)
				self.currentFile = file
				tkImage = ImageTk.PhotoImage(image)
				label_image = Tkinter.Label(root, image=tkImage)
				label_image.place(x=0,y=0,width=image.size[0],height=image.size[1])
				root.geometry('%dx%d' % (image.size[0],image.size[1]))
				root.mainloop()
			except:
				pass

	#Closes TkInter window on key press
	def exit_mainloop(self, event):
		print self.currentFileNum
		if event.keysym == 'a':
			self.labelImage(self.currentFile, 'apple')
		elif event.keysym == 'o':
			self.labelImage(self.currentFile, 'orange')
		elif event.keysym == 'space':
			pass	#skips labeling this image
		event.widget.quit()

	def labelImage(self, imageFile, label):
		lastSlashIndex = imageFile.rfind('/')
		fileTypeIndex = imageFile.rfind('.jpeg')
		metadataFilePath = imageFile[:lastSlashIndex] + '/meta' + imageFile[lastSlashIndex+1:fileTypeIndex] + '..json'
		print metadataFilePath
		try:
			metadata = json.loads(readData(metadataFilePath))
			trainingDatum = {
				'imageFilePath': imageFile,
				'rMean': metadata['features']['rMean'],
				'gMean': metadata['features']['gMean'],
				'bMean': metadata['features']['bMean'],
				'rStdDev': metadata['features']['rStdDev'],
				'gStdDev': metadata['features']['gStdDev'],
				'bStdDev': metadata['features']['bStdDev'],
				'apple/orange': label
			}
			writeToCSV(self.fileName, self.fieldnames, trainingDatum)
		except:
			pass

#Generates a random sample of images to 
#manually classify for training data
def generateRandomSampleImages(dataDir, numImages):
	completeBuildingImages = getCompleteBuildingImages(dataDir)
	randomSample = random.sample(completeBuildingImages, numImages)
	return randomSample

def generateCompleteImageSet(dataDir):
	completeImages = getCompleteBuildingImages(dataDir)
	return completeImages

def getCompleteBuildingImages(dataDir):
	completeBuildingImages = []
	buildingsPath = os.listdir(dataDir)
	for img in buildingsPath:
		try:
			if img[-4:] == 'jpeg':
				imagePath = dataDir + img
				completeBuildingImages.append(imagePath)
		except:
			pass
	return completeBuildingImages

def readData(source):
	with open(source, 'r') as f:
		content = f.read()
	return content

def setHeaders(target, fieldnames):
	with open(target, 'a') as f:
		writer = csv.DictWriter(f, fieldnames)
		writer.writeheader()

def writeToCSV(target, fieldnames, content):
	with open(target, 'a') as csvfile:
	    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	    writer.writerow(content)

def main():
	#imageSample = generateRandomSampleImages('data/', 500)
	imageSample = generateCompleteImageSet('training/')
	print imageSample
	trainer = Trainer()
	trainer.generateTrainingDataLabels(imageSample)

if __name__ == '__main__':
	main()
