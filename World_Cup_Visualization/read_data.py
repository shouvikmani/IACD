from time import time
from csv import DictReader
'''
def parseTweetIdCSV(source):
	with open(source, 'r') as csvfile:
		reader = DictReader(csvfile)
	print reader
	return reader
'''
def readFile(source):
	with open(source, 'r') as f:
		data = f.read()
	return data

#TODO: Use yield generators here
#TODO: Fix '"' formatting issue with outer calling function
#      generating values on the fly
def parseTweetIdCSV(source):
	start = time()
	data = readFile(source)
	print "Read file time: " + str(time() - start)
	dataLines = data.splitlines()
	print "Split lines time: " + str(time() - start)
	dataList = []
	for i in xrange(1, 101):
		instanceDict = dict()
		instance = dataLines[i].split()
		#Removing " because id formatted as '"id"' in tweets.csv
		instanceDict['id'] = instance[0].replace('"', '')
		dataList.append(instanceDict)
	print "Parsing csv time: " + str(time() - start)
	return dataList
