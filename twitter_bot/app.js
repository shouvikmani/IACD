var fs = require('fs');
var util = require('util');
var request = require('request');
var Twitter = require('twitter');
var markov = require('markov');
var config = require('./config');

console.log("Starting Twitter Bot Transmission");

var auth = new Buffer([config.bingAccountKey, config.bingAccountKey].join(':')).toString('base64');
var rootUrl = 'https://api.datamarket.azure.com/Bing/Search';
var searchFilter = '/Image?$top=60&Query='
var query = 'Donald Trump';

request({
    url : rootUrl + searchFilter + query,
    method: 'GET',
    headers: {
     	'Authorization' : 'Basic ' + auth
    },
    qs  : {
      $format : 'json',
      Query   : "'" + query + "'", // the single quotes are required!
    }
  }, function(error, response, body) {
    if (error) {
      console.log(error)
    } else {
    	processSearchResponse(response.body);
    }
});

function processSearchResponse(data) {
	var results = parseImageData(data);
	var selectedImage = selectRandomImage(results);
	var imagePath = downloadImage(selectedImage);
}

function parseImageData(data) {
	var dataJSON = JSON.parse(data);
	var results = dataJSON['d']['results'];
	return results;
}

function selectRandomImage(results) {
	//random number between 0 and length of results array
	var randomInt = Math.floor(Math.random() * (results.length - 0));
	return results[randomInt];
}

function downloadImage(image) {
	var imageUrl = image['MediaUrl'];
	var download = function(uri, filename, callback){
	  request.head(uri, function(err, res, body){
	    request(uri).pipe(fs.createWriteStream(filename)).on('close', callback);
	  });
	};

	download(imageUrl, './imageDir/twitter_img', function(){
		makeTwitterPost('./imageDir/twitter_img');
	});
}

function makeTwitterPost(imagePath) {
	var client = twitterAuthenticate();
	var image = fs.readFileSync('./imageDir/twitter_img');
	var postImage = function(markovText) {
		client.post('media/upload', {media: image}, function(error, media, response){
		  if (!error) {
		    var status = {
		      status: markovText,
		      media_ids: media.media_id_string // Pass the media id string
		    }
		    client.post('statuses/update', status, function() {
		    	if (!error) {
		    		console.log('Post succuessful!');
		    	}
		    });
		  }
		});
	}
	generateMarkovText(postImage);
}

function twitterAuthenticate() {
	var client = new Twitter({
	  consumer_key: config.twitterConsumerKey,
	  consumer_secret: config.twitterConsumerSecret,
	  access_token_key: config.twitterAccessToken,
	  access_token_secret: config.twitterAccessTokenSecret
	});
	return client;
}

function generateMarkovText(callback) {
	var m = markov(4);
	var s = fs.readFileSync('donald_corpus.txt');
	m.seed(s, function(){
		var markovText = m.respond('', 4).join(' ');
		var lastPeriodIndex = markovText.lastIndexOf('.')
		if (lastPeriodIndex != -1) {
			markovText = markovText.slice(0, lastPeriodIndex + 1);
		}
		callback(markovText);
	});
}