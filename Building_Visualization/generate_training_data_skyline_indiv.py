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
		self.fieldnames = ['imageFilePath','rMean','gMean','bMean', 
							'rStdDev','gStdDev','bStdDev','skyline/individual']

	#Runs GUI that lets user classify images to
	#create labels for training data
	def generateTrainingDataLabels(self, randomImageSample):
		setHeaders('training_data/skylineIndividual.csv', self.fieldnames)
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
		if event.keysym == 's':
			self.labelImage(self.currentFile, 'skyline')
		elif event.keysym == 'i':
			self.labelImage(self.currentFile, 'individual')
		elif event.keysym == 'space':
			pass	#skips labeling this image
		event.widget.quit()

	def labelImage(self, imageFile, label):
		lastSlashIndex = imageFile.rfind('/')
		fileTypeIndex = imageFile.rfind('.jpg')
		metadataFilePath = imageFile[:lastSlashIndex] + '/meta' + imageFile[lastSlashIndex+1:fileTypeIndex] + '.json'
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
				'skyline/individual': label
			}
			writeToCSV('training_data/skylineIndividual.csv', self.fieldnames, trainingDatum)
		except:
			pass

#Generates a random sample of images to 
#manually classify for training data
def generateRandomSampleImages(dataDir, numImages):
	completeBuildingImages = getCompleteBuildingImages(dataDir)
	randomSample = random.sample(completeBuildingImages, numImages)
	return randomSample

def getCompleteBuildingImages(dataDir):
	completeBuildingImages = []
	buildingsPath = os.listdir(dataDir)
	for building in buildingsPath:
		try:
			buildingImagesPath = dataDir + building + '/'
			buildingImages = os.listdir(buildingImagesPath)
			for img in buildingImages:
				if img[-4:] == '.jpg':
					imagePath = buildingImagesPath + img
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
	randomImageSample = generateRandomSampleImages('data/', 500)
	trainer = Trainer()
	trainer.generateTrainingDataLabels(randomImageSample)

if __name__ == '__main__':
	main()
