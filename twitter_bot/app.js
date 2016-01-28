var fs = require('fs');
var request = require('request');
var config = require('./config');

console.log("Starting Twitter Bot Transmission");

var auth = new Buffer([config.bingAccountKey, config.bingAccountKey].join(':')).toString('base64');
var rootUrl = 'https://api.datamarket.azure.com/Bing/Search';
var searchFilter = '/Image?$top=60&Query='
var query = 'Donald Trump';

//Fetching Data from Bing Search API
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
	console.log(imagePath);
}
