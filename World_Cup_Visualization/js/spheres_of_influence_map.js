var spheres = [];
var mapBubbles = [];
var show25PercentSphere = true;
var show50PercentSphere = false;
var show75PercentSphere = false;

var map = new Datamap({
    element: document.getElementById('spheresOfInfluenceMap'),
    scope: 'world',
    projection: 'mercator',
    responsive: true,
    geographyConfig: {
        highlightOnHover: false
    },
    bubblesConfig: {
    	highlightOnHover: false,
    	popupTemplate: function(geography, data) {
          return '';
        },
    },
    fills: {
        defaultFill: '#aaaaaa',
    },
    done: function(datamap) {
        datamap.svg.selectAll('.datamaps-subunit').on('mouseenter', function(geography) {
            addSphereToMap(geography.id);
        });
        datamap.svg.selectAll('.datamaps-subunit').on('mouseleave', function(geography) {
        	//Check that not hovering over a bubble first
            if ($('.bubbles:hover').length == 0) {
			    removeSphereFromMap();
			}
        });
    }
});

setupSpheresOfInfluence(jsonData);

function setupSpheresOfInfluence(countries) {
	var countryFills = {};
	for (var i = 0; i < countries.length; i++) {
		map.options.fills[countries[i]["code"]] = countries[i]["color"];
		countryFills[countries[i]["code"]] = countries[i]["color"];
		//Adds a sphere for 25%, 50%, 75%
		countrySpheres = [{
			'id': countries[i]['code'],
			'fillKey': countries[i]['code'],
			'name': '25%_distance',
			'radius': countries[i]['25%_distance']/50,	//Divide by 50 to scale down to pixels
			'latitude': countries[i]['coordinates'][0],
			'longitude': countries[i]['coordinates'][1],
			'fillOpacity': 0.75
		}, {
			'id': countries[i]['code'],
			'fillKey': countries[i]['code'],
			'name': '50%_distance',
			'radius': countries[i]['50%_distance']/50,
			'latitude': countries[i]['coordinates'][0],
			'longitude': countries[i]['coordinates'][1],
			'fillOpacity': 0.50
		}, {
			'id': countries[i]['code'],
			'fillKey': countries[i]['code'],
			'name': '75%_distance',
			'radius': countries[i]['75%_distance']/50,
			'latitude': countries[i]['coordinates'][0],
			'longitude': countries[i]['coordinates'][1],
			'fillOpacity': 0.25
		}]
		spheres = spheres.concat(countrySpheres);
	}
	map.updateChoropleth(countryFills);
}

function addSphereToMap(countryId) {
	removeSphereFromMap();
	for (var i = 0; i < spheres.length; i++) {
		if (spheres[i]['id'] == countryId) {
			if (show25PercentSphere == true && spheres[i]['name'] == '25%_distance') {
				mapBubbles.push(spheres[i]);
			}
			if (show50PercentSphere == true && spheres[i]['name'] == '50%_distance') {
				mapBubbles.push(spheres[i]);
			}
			if (show75PercentSphere == true && spheres[i]['name'] == '75%_distance') {
				mapBubbles.push(spheres[i]);
			}
		}
	}
	map.bubbles(mapBubbles);
}

function removeSphereFromMap() {
	mapBubbles = []
	map.bubbles(mapBubbles);
}

function toggle25PercentButton() {
	if (show25PercentSphere == true) { 
		show25PercentSphere = false;
		$('#percent25Button').css('background', '#fff');
	} else {
		show25PercentSphere = true;
		$('#percent25Button').css('background', '#eee');
	}
}

function toggle50PercentButton() {
	if (show50PercentSphere == true) { 
		show50PercentSphere = false;
		$('#percent50Button').css('background', '#fff');
	} else {
		show50PercentSphere = true;
		$('#percent50Button').css('background', '#eee');
	}
}

function toggle75PercentButton() {
	if (show75PercentSphere == true) { 
		show75PercentSphere = false;
		$('#percent75Button').css('background', '#fff');
	} else {
		show75PercentSphere = true;
		$('#percent75Button').css('background', '#eee');
	}
}

window.addEventListener('resize', function() {
    map.resize();
});
