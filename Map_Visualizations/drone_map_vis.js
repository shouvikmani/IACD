//Initialize Leaflet map and styles
var map = L.map('map').setView([17.64, 53.61], 4);
var CartoDB_DarkMatter = L.tileLayer('http://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png', {
	attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions">CartoDB</a>',
	subdomains: 'abcd',
	maxZoom: 19
}).addTo(map);

$.ajax({
	type: 'GET',
    url: 'http://api.dronestre.am/data',
    contentType: "application/json",
    dataType: 'jsonp',
    success: function(json) {
       console.log(json);
       strikeData = json['strike'];
       plotMarkers(strikeData);
       addSatImages(strikeData);
    },
    error: function(e) {
       console.log(e.message);
    }
})

function plotMarkers(data) {
	var marker;
	for (var i = 0; i < data.length; i++) {
		var strikeLat = data[i]['lat'];
		var strikeLon = data[i]['lon'];
		var region = data[i]['location'];
		var country = data[i]['country'];
		var date = getLocalDate(data[i]['date']);
		var narrative = data[i]['narrative'];
		var deaths = data[i]['deaths'];
		var injuries = data[i]['injuries'];

		marker = L.marker([strikeLat, strikeLon], {icon: getMarkerIcon(country)}).addTo(map);
		marker.bindPopup("<b>Location: </b>" + region + ", " + country
						+ "<br><b>Date: </b>" + date
						+ "<br>" + narrative
						+ "<br><br>"
						+ "<b>Deaths: </b>" + deaths
						+ "&nbsp;&nbsp;|&nbsp;&nbsp;"
						+ "<b>Injuries: </b>" + injuries);
	}
}

//Converts an ISO date time value to a local date time string 
function getLocalDate(isoDateTime) {
	var utcDate = new Date(isoDateTime);
	var localDate = utcDate.toLocaleString();

	return localDate;
}

function getMarkerIcon(country) {
	if (country === 'Somalia') {
		return L.icon({iconUrl: 'static/blue_marker.svg'});
	} else if (country === 'Yemen') {
		return L.icon({iconUrl: 'static/red_marker.svg'});
	} else if (country == 'Pakistan' || country === 'Pakistan-Afghanistan Border') {
		return L.icon({iconUrl: 'static/green_marker.svg'});
	} else {
		return L.icon({iconUrl: 'static/white_marker.svg'});
	}
}

function addSatImages(data) {
	var googleMapsApiKey = 'AIzaSyBLtOssY47tO3dbrV6liAY5X7LhVjTaNw8'
	var zoomLevel = '17';
	var googleMapsRootURL = 'https://maps.googleapis.com/maps/api/staticmap?';
	var size = '220x220';
	var mapType = 'satellite';
	for (var i = data.length - 1; i > -1; i--) {
		var strikeLat = data[i]['lat'];
		var strikeLon = data[i]['lon'];

		var mapURL = googleMapsRootURL + 'center=' + strikeLat + ',' + strikeLon
						+ '&zoom=' + zoomLevel + '&size=' + size + '&maptype='
						+ mapType + '&key=' + googleMapsApiKey;
		console.log(mapURL);
		$('#sat-image-grid').append('<img class="sat-image" src=' + mapURL + '>');
	}
}

//Hides bottom label
document.getElementsByClassName('leaflet-control-attribution leaflet-control')[0].style.display = 'none';
