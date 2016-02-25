#!/usr/bin/env python

import requests
import urllib
import json
import datetime
from pprint import pprint
from time import time

from twitter_auth import authenticate
from read_data import parseTweetIdCSV

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

def getTweets(tweetIdList):
	base_url = 'https://api.twitter.com/1.1/statuses/lookup.json?'
	idList = [tweet['id'] for tweet in tweetIdList]
	idListString = ','.join(idList)
	params = {'id': idListString}
	paramsEncode = urllib.urlencode(params)
	query_url = base_url + paramsEncode
	tweets = getRequest(query_url)
	#Filters to only geotagged tweets
	geoTweets = filter(lambda x: str(x['coordinates']) != 'None', tweets)
	return geoTweets

def main():
	#start = time()
	tweetData = parseTweetIdCSV('data/tweets.csv')
	#print "Parsing time: " + str(time() - start)
	pprint(getTweets(tweetData))
	#print "API Request time: " + str(time() - start)
	print getRateLimit()

main()
