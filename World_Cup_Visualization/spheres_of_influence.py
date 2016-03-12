import pprint
from read_data import readCSVFile, readJSONFile, writeJSONFile

#Returns the radius of the sphere of influence within which
#the desiredPercentage of tweets are posted
def getSphereRadius(tweetsAboutCountry, desiredPercentage):
	totalTweets = len(tweetsAboutCountry)
	edgeTweetIndex = int(round(float(desiredPercentage)/100 * totalTweets))
	edgeTweetDistance = tweetsAboutCountry[edgeTweetIndex]['distanceFromCountry']
	return edgeTweetDistance

def calculateSpheresOfInfluence(countryInfo, tweetsAboutCountryBasePath):
	spheresOfInfluence = []
	for country in countryInfo:
		tweetsAboutCountryFilePath = tweetsAboutCountryBasePath + country["Name"] + '_tweets.csv'
		tweetsAboutCountry = readCSVFile(tweetsAboutCountryFilePath)
		countryInfluence = {
			'name': country['Name'],
			'coordinates': country['Coordinates'],
			'code': country['Code'],
			'color': country['Color'],
			'25%_distance': getSphereRadius(tweetsAboutCountry, 25),
			'50%_distance': getSphereRadius(tweetsAboutCountry, 50),
			'75%_distance': getSphereRadius(tweetsAboutCountry, 75)
		}
		spheresOfInfluence.append(countryInfluence)
	return spheresOfInfluence

def main():
	countryInfoFilePath = 'data/countries.json'
	countryInfo = readJSONFile(countryInfoFilePath)
	tweetsAboutCountryBasePath = 'data/Tweets_About_Country/'
	spheresOfInfluence = calculateSpheresOfInfluence(countryInfo, tweetsAboutCountryBasePath)
	writeJSONFile(spheresOfInfluence, 'data/spheresOfInfluence.json')

if __name__ == '__main__':
	main()
