import json
from csv import DictReader, DictWriter

def readFile(source):
	with open(source, 'r') as f:
		data = f.read()
	return data

def readJSONFile(source):
	with open(source, 'r') as f:
		data = json.load(f)
	return data

def writeJSONFile(data, source):
	with open(source, 'w') as f:
		json.dump(data, f)

def readCSVFile(source):
	csvData = []
	with open(source) as f:
		reader = DictReader(f)
		for row in reader:
			csvData.append(row)
	return csvData

def writeToFile(data, source, fieldnames):
	with open(source, 'a') as f:
		writer = DictWriter(f, fieldnames)
		for row in data:
			writer.writerow(row)

def setHeaders(source, fieldnames):
	with open(source, 'w') as f:
		writer = DictWriter(f, fieldnames)
		writer.writeheader()
