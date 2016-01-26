console.log("HI");
mapboxgl.accessToken = 'pk.eyJ1Ijoic2hvdXZpa21hbmkiLCJhIjoiY2lqdmx6a3VhMDh0Y3VjbTVycXV2MW0xNiJ9.4MgtlH94XYLTO3TPEtqIbw';
var map = new mapboxgl.Map({
    container: 'map', // container id
    style: 'mapbox://styles/mapbox/streets-v8', //stylesheet location
    center: [53.61, 17.64], // [longitude, latitude] order
    zoom: 3 // starting zoom
});