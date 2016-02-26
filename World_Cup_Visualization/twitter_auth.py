import requests
import urllib
import base64
import json

import config

#Returns bearer token for authorization given
#which API key to use (apiKeyNum)
def authenticate(apiKeyNum):
	authUrl = 'https://api.twitter.com/oauth2/token'
	base64Credentials = encodeCredentials(apiKeyNum)
	headers = ({
		'Authorization': 'Basic %s'  % base64Credentials, 
		'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
	})
	data = {'grant_type': 'client_credentials'}
	r = requests.post(authUrl, headers=headers, data=data)
	bearerToken = json.loads(r.text)['access_token']
	return bearerToken

#Coverts consumer key and secret to base64 encoding
def encodeCredentials(apiKeyNum):
	APITokensDict = config.APITokens[apiKeyNum-1]
	keyEncode = urllib.quote(APITokensDict['CONSUMER_KEY'])
	secretEncode = urllib.quote(APITokensDict['CONSUMER_SECRET'])
	tokenCredentials = keyEncode + ':' + secretEncode
	return base64.b64encode(tokenCredentials)
