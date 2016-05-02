import os
import sys
import json
from PIL import Image, ImageStat

#Adds image feature information to the metadata
#JSON file for each image in imageDir
def generateImageFeatures(imageDir):
	imageDirPath = 'data/' + imageDir
	files = os.listdir(imageDirPath)
	for f in files:
		imageFilePath = imageDirPath + '/' + f
		try:
			image = Image.open(imageFilePath)
			stat = ImageStat.Stat(image)
			pixelMean = stat.mean
			pixelStdDev = stat.stddev
			saveJSONMetaData(imageDirPath, f, pixelMean, pixelStdDev)
		except:
			pass

def saveJSONMetaData(imageDirPath, fileName, pixelMean, pixelStdDev):
	fileNameFormatted = fileName[:-4]	#Removes '.jpg' file type
	metadataFilePath = imageDirPath + '/' + 'meta' + fileNameFormatted + '.json'
	metadata = {
		'features' : {
			'rMean': pixelMean[0],
			'gMean': pixelMean[1],
			'bMean': pixelMean[2],
			'rStdDev': pixelStdDev[0],
			'gStdDev': pixelStdDev[1],
			'bStdDev': pixelStdDev[2]
		}
	}
	with open(metadataFilePath, 'a') as f:
		f.write(json.dumps(metadata))

def main():
	imageDir = sys.argv[1]
	generateImageFeatures(imageDir)

if __name__ == '__main__':
	main()
