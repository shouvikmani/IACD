//Initialize Leaflet map and styles
var map = L.map('map').setView([17.64, 53.61], 4);
var CartoDB_DarkMatter = L.tileLayer('http://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png', {
	attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions">CartoDB</a>',
	subdomains: 'abcd',
	maxZoom: 19
}).addTo(map);

//Hides bottom label
document.getElementsByClassName('leaflet-control-attribution leaflet-control')[0].style.display = 'none';