#!/usr/bin/env python

import requests
import urllib
import json
import datetime
import sys
from pprint import pprint
from time import time

from twitter_auth import authenticate
from read_data import readFile, writeToFile, setHeaders

#Token global variable
bearerToken = authenticate()

def getRequest(query_url):
	headers = ({
		'Authorization': 'Bearer %s'  % bearerToken, 
		'Content-Type': 'application/json'
	})
	r = requests.get(query_url, headers=headers)
	data = json.loads(r.text)
	return data

def getRateLimit():
	base_url = 'https://api.twitter.com/1.1/application/rate_limit_status.json?'
	params = {'resources': 'statuses'}
	paramsEncode = urllib.urlencode(params)
	query_url = base_url + paramsEncode
	rateLimitStatus = getRequest(query_url)
	return rateLimitStatus

#Takes a query and count of tweets (up to 100)
#Returns list of recent tweets for query
def twitter_search(query, count, since, until):
	base_url = 'https://api.twitter.com/1.1/search/tweets.json?'
	params = {
		'q': query, 
		'result_type': 'recent', 
		'count': count,
		'until': until,
		'since': since
	}
	filtersEncode = urllib.urlencode(params)
	search_url = base_url + filtersEncode
	result = getRequest(search_url)
	search_results = []
	for r in result['statuses']:
		search_results.append((r['created_at'], r['id']))
	return search_results

def getFollowerCount(screenName):
	base_url = 'https://api.twitter.com/1.1/users/show.json?'
	params = {'screen_name': screenName}
	paramsEncode = urllib.urlencode(params)
	query_url = base_url + paramsEncode
	followerCount = getRequest(query_url)['followers_count']
	return followerCount

def getTweetsFromId(tweetIdList):
	base_url = 'https://api.twitter.com/1.1/statuses/lookup.json?'
	idList = [tweet['id'] for tweet in tweetIdList]
	idListString = ','.join(idList)
	params = {'id': idListString}
	paramsEncode = urllib.urlencode(params)
	query_url = base_url + paramsEncode
	tweets = getRequest(query_url)
	#Filters to only geotagged tweets
	geoTweets = filter(lambda x: str(x['coordinates']) != 'None', tweets)
	reducedTweets = [
		{
			'id_str': tweet['id_str'],
			'created_at': tweet['created_at'],
			'coordinates': tweet['coordinates'],
			'hashtags': tweet['entities']['hashtags'],
			'text': tweet['text'].encode('ascii', 'ignore')
		} for tweet in geoTweets
	]
	return reducedTweets

#Parses and returns a list of tweetIDs from a list of data
#starting at startRow and ending at endRow
def parseTweetIds(dataLines, startRow, endRow):
	start = time()
	dataList = []
	for i in xrange(startRow, endRow+1):
		instanceDict = dict()
		instance = dataLines[i].split()
		#Removing " because id formatted as '"id"' in tweets.csv
		instanceDict['id'] = instance[0].replace('"', '')
		dataList.append(instanceDict)
	return dataList

#TODO: Use end to enforce upper limit on requestEndRow
def downloadAllTweets(start, end):
	requestStartRow = start
	requestEndRow = start + 99
	numRequests = 0
	tweetIdSource = 'data/tweets.csv'
	tweetTargetSource = 'data/completeTweets.csv'
	dataLines = readFile(tweetIdSource).splitlines()
	fieldnames = ['id_str', 'created_at', 'coordinates', 'hashtags', 'text']
	setHeaders(tweetIdSource, fieldnames)
	while (numRequests < 60):
		tweetIdList = parseTweetIds(dataLines, requestStartRow, requestEndRow)
		tweetData = getTweetsFromId(tweetIdList)
		print tweetData
		print numRequests
		print
		writeToFile(tweetData, tweetTargetSource, fieldnames)
		requestStartRow += 100
		requestEndRow += 100
		numRequests += 1
	print getRateLimit()

def main():
	start = time()
	startRow = int(sys.argv[1])
	endRow = int(sys.argv[2])
	downloadAllTweets(startRow, endRow)

if __name__ == '__main__':
	main()
