from time import time
from csv import DictReader, DictWriter

def readFile(source):
	with open(source, 'r') as f:
		data = f.read()
	return data

def writeToFile(data, source, fieldnames):
	with open(source, 'a') as f:
		writer = DictWriter(f, fieldnames)
		writer.writeheader()
		for row in data:
			writer.writerow(row)

def setHeaders(source, fieldnames):
	with open(source, 'w') as f:
		writer = DictWriter(f, fieldnames)
		writer.writeheader()
