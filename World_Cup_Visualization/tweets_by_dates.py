from read_data import readJSONFile, readCSVFile
from dateutil.parser import parse
from pprint import pprint

def getTweetDateStats(datesSet, countryInfo):
	tweetsAboutCountryBasePath = 'data/Tweets_About_Country/'
	tweetDateInfoDict = dict()
	for date in datesSet:
		tweetDateInfoDict[date] = dict()
	for country in countryInfo:
		completeCountryFilePath = tweetsAboutCountryBasePath + country["Name"] + '_tweets.csv'
		countryTweets = readCSVFile(completeCountryFilePath)
		#TODO: Finish this code

def getAllDates(countryInfo):
	tweetsAboutCountryBasePath = 'data/Tweets_About_Country/'
	dates = set()
	for country in countryInfo:
		completeCountryFilePath = tweetsAboutCountryBasePath + country["Name"] + '_tweets.csv'
		countryTweets = readCSVFile(completeCountryFilePath)
		for tweet in countryTweets:
			tweetDateTime = parse(tweet["created_at"])
			tweetDate = tweetDateTime.date()
			dates.add(tweetDate)
	return sorted(list(dates))

def main():
	countryInfoFilePath = 'data/countries.json'
	countryInfo = readJSONFile(countryInfoFilePath)
	datesSet = getAllDates(countryInfo)
	tweetDateStats = getTweetDateStats(datesSet, countryInfo)
	print len(datesSet)
	pprint(datesSet)

if __name__ == '__main__':
	main()
