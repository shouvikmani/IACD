import sys
import os
from urllib2 import urlopen
from urllib import urlretrieve
from BeautifulSoup import BeautifulSoup

def scrapeBuildingImages(buildingName, buildingUrl, numPages):
	os.mkdir('data/' + buildingName)
	mainPage = urlopen(buildingUrl)
	mainSoup = BeautifulSoup(mainPage)
	index = 0
	for i in xrange(1, numPages+1):
		print "Scraping page: " + str(i) + ' out of ' + str(numPages)
		pageUrl = buildingUrl + '&page=' + str(i)
		page = urlopen(pageUrl)
		pageSoup = BeautifulSoup(page)
		#Finds all img tags
		images = pageSoup.findAll('img')
		for img in images:
			index += 1
			if 'http' in img['src']:
				targetPath = 'data/' + buildingName + '/' + str(index) +'.jpg'
				try:
					urlretrieve(img['src'], targetPath)
				except:
					continue

#Deletes any files less than 5000 bytes
def deletePoorImages(buildingName):
	imageDirPath = 'data/' + buildingName
	files = os.listdir(imageDirPath)
	for f in files:
		filePath = imageDirPath + '/' + f
		fileSize = os.stat(filePath).st_size
		if fileSize < 5000:
			os.remove(filePath)

def main():
	buildingName = sys.argv[1]
	buildingUrl = sys.argv[2]
	numPages = int(sys.argv[3])
	scrapeBuildingImages(buildingName, buildingUrl, numPages)
	deletePoorImages(buildingName)

if __name__ == '__main__':
	main()
