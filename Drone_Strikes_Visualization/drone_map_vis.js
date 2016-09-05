//Initialize Leaflet map and styles
var map = L.map('map').setView([17.64, 53.61], 4);
var CartoDB_DarkMatter = L.tileLayer('http://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png', {
	attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions">CartoDB</a>',
	subdomains: 'abcd',
	maxZoom: 19
}).addTo(map);

//AJAX Request to get drone strike data
$.ajax({
	type: 'GET',
    url: 'http://api.dronestre.am/data',
    contentType: "application/json",
    dataType: 'jsonp',
    success: function(json) {
       strikeData = json['strike'];
       plotMarkers(strikeData);
       addSatImages(strikeData);
    },
    error: function(e) {
       console.log(e.message);
    }
});

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

		try {
			marker = L.marker([strikeLat, strikeLon], {icon: getMarkerIcon(country)}).addTo(map);
			marker.bindPopup("<b>Location: </b>" + region + ", " + country
							+ "<br><b>Date: </b>" + date
							+ "<br>" + "<b>Narrative: </b>" + narrative
							+ "<br><br>"
							+ "<b>Deaths: </b>" + deaths
							+ "&nbsp;&nbsp;|&nbsp;&nbsp;"
							+ "<b>Injuries: </b>" + injuries);
		} catch(err) {
			continue;
		}
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

//Adds a grid of static sattelite imagery
function addSatImages(data) {
	$.ajaxSetup({async: false});
	var googleMapsApiKey;
	$.getJSON('config.json', function(data) {
		googleMapsApiKey = data['google_maps_API_key'];
	});
	$.ajaxSetup({async: true});
	var zoomLevel = '17';
	var googleMapsRootURL = 'https://maps.googleapis.com/maps/api/staticmap?';
	var size = '220x220';
	var mapType = 'satellite';
	for (var i = data.length - 1; i > -1; i--) {
		var strikeLat = data[i]['lat'];
		var strikeLon = data[i]['lon'];
		var region = data[i]['location'];
		var country = data[i]['country'];
		var date = getLocalDate(data[i]['date']);
		var narrative = data[i]['narrative'];
		var deaths = data[i]['deaths'];
		var injuries = data[i]['injuries'];

		if (strikeLat != "" && strikeLon != "") {
			var mapURL = googleMapsRootURL + 'center=' + strikeLat + ',' + strikeLon
							+ '&zoom=' + zoomLevel + '&size=' + size + '&maptype='
							+ mapType + '&key=' + googleMapsApiKey;
			$('#sat-image-grid').append(
				'<div class="sat-image-container">' +
					'<div class="sat-image-overlay">' +
						'<div class="sat-image-overlay-text">' +
							"<b>Location: </b>" + region + ", " + country
							+ "<br>"
							+ "<br><b>Date: </b>" + date
							+ "<br>" + "<b>Narrative: </b>" + narrative
							+ "<br><br>"
							+ "<b>Deaths: </b>" + deaths
							+ "&nbsp;&nbsp;|&nbsp;&nbsp;"
							+ "<b>Injuries: </b>" + injuries +
						'</div>' +
					'</div>' +
					'<img class="sat-image" src=' + mapURL + '>' +
				'<div>'
			);
		}
	}
}

//Hides bottom label
$('.leaflet-control-attribution').hide();
//Sets map height to 80% of screen height
//(had troubles directly with css)
$('#map').height(function() {
	return (window.innerHeight * 0.75) + 'px';
});
map.invalidateSize(true);
