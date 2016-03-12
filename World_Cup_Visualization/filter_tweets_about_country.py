import json
import pprint

from haversine import haversine
from copy import deepcopy
from read_data import readFile, readJSONFile, readCSVFile, writeToFile, setHeaders

def saveTweetsToFile(tweetsAboutCountries, targetFileBasePath):
	fieldnames = ['id_str', 'created_at', 'coordinates', 'hashtags', 'text', 'distanceFromCountry']
	for country in tweetsAboutCountries:
		countryFilePath = targetFileBasePath + country + '_tweets.csv'
		setHeaders(countryFilePath, fieldnames)
		writeToFile(tweetsAboutCountries[country], countryFilePath, fieldnames)

#Checks if the tweet contains text or hashtag about country
def isAboutCountry(tweet, country):
	for term in country['Terms']:
		if term in tweet['text']:
			return True
	if country['Hashtag'] in tweet['hashtags']:
		return True
	return False

def filterCountryTweets(completeTweets, countryInfo):
	tweetsAboutCountries = dict()
	for country in countryInfo:
		tweetsAboutCountry = []
		for tweet in completeTweets:
			if (isAboutCountry(tweet, country)):
				tweetLat = eval(tweet['coordinates'])['coordinates'][1]
				tweetLong = eval(tweet['coordinates'])['coordinates'][0]
				tweetCoords = (tweetLat, tweetLong)
				countryCoords = tuple(country['Coordinates'])
				tweet['distanceFromCountry'] = haversine(tweetCoords, countryCoords)	#distance in km
				tweetsAboutCountry.append(tweet)
		tweetsAboutCountries[country['Name']] = deepcopy(sorted(tweetsAboutCountry, 
													key=lambda tweet: tweet['distanceFromCountry']))
	return tweetsAboutCountries

def getCombinedTweets():
	completeTweetsBasePath = 'data/Complete_Tweets/completeTweets'
	combinedCompleteTweets = []
	fieldnames = ['id_str', 'created_at', 'coordinates', 'hashtags', 'text']
	for i in xrange(1, 26):
		completeTweetsFilePath = completeTweetsBasePath + str(i) + '.csv'
		completeTweets = readCSVFile(completeTweetsFilePath)
		for tweet in completeTweets:
			tweetDict = {
				'id_str': tweet['id_str'],
				'created_at': tweet['created_at'],
				'coordinates': tweet['coordinates'],
				'hashtags': tweet['hashtags'],
				'text': tweet['text'].lower()
			}
			combinedCompleteTweets.append(tweetDict)
	return combinedCompleteTweets

def main():
	countryInfoFilePath = 'data/countries.json'
	countryInfo = readJSONFile(countryInfoFilePath)
	combinedCompleteTweets = getCombinedTweets()
	tweetsAboutCountries = filterCountryTweets(combinedCompleteTweets, countryInfo)
	saveTweetsToFile(tweetsAboutCountries, 'data/Tweets_About_Country/')

if __name__ == '__main__':
	main()
