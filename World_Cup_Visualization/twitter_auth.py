import requests
import urllib
import base64
import json

import config

#Returns bearer token for authorization
def authenticate():
	authUrl = 'https://api.twitter.com/oauth2/token'
	base64Credentials = encodeCredentials()
	headers = ({
		'Authorization': 'Basic %s'  % base64Credentials, 
		'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
	})
	data = {'grant_type': 'client_credentials'}
	r = requests.post(authUrl, headers=headers, data=data)
	bearerToken = json.loads(r.text)['access_token']
	return bearerToken

#Coverts consumer key and secret to base64 encoding
def encodeCredentials():
	keyEncode = urllib.quote(config.CONSUMER_KEY)
	secretEncode = urllib.quote(config.CONSUMER_SECRET)
	tokenCredentials = keyEncode + ':' + secretEncode
	return base64.b64encode(tokenCredentials)
