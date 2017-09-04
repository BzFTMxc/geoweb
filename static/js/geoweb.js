/**
 * geoweb.js
 * Author: Abhay Arora (@BzFTMxc)
 */

_A = angular.module('geoweb', ['ngRoute']);

_A.config(['$routeProvider', '$locationProvider', function($routeProvider,
							   $locationProvider) {
    $routeProvider.when('/', {
	redirectTo: '/network-tools'
    }).when('/network-tools', {
	controller: 'NetworkTools',
	templateUrl: '/view/network-tools'
    }).otherwise({
	redirectTo: '/'
    });
}]);


_A.controller('NetworkTools', ['$scope', '$http', function($scope, $http) {

    // Render Map
    var map_style_definition = [
	{
            "featureType": "landscape.man_made",
            "elementType": "geometry.fill",
            "stylers": [
		{
                    "color": "#f5f9fa"
		},
		{
                    "weight": 1.01
		},
		{
                    "lightness": -6
		}
            ]
	},
	{
            "featureType": "landscape.man_made",
            "elementType": "geometry.stroke",
            "stylers": [
		{
                    "color": "#4c6dab"
		},
		{
                    "weight": 0.85
		},
		{
                    "saturation": -56
		},
		{
                    "lightness": 39
		},
		{
                    "gamma": 1.71
		}
            ]
	},
	{
            "featureType": "administrative.country",
            "elementType": "geometry.stroke",
            "stylers": [
		{
                    "color": "#2c4785"
		},
		{
                    "weight": 1
		}
            ]
	},
	{
            "featureType": "administrative.locality",
            "elementType": "labels.text.fill",
            "stylers": [
		{
                    "color": "#292929"
		}
            ]
	},
	{
            "featureType": "poi.school",
            "elementType": "labels.text.fill",
            "stylers": [
		{
                    "visibility": "on"
		},
		{
                    "color": "#0e2392"
		}
            ]
	},
	{
            "featureType": "poi",
            "elementType": "labels.text.fill",
            "stylers": [
		{
                    "color": "#595959"
		}
            ]
	},
	{
            "featureType": "poi",
            "elementType": "labels.text.stroke",
            "stylers": [
		{
                    "visibility": "on"
		},
		{
                    "color": "#e0f3ff"
		}
            ]
	},
	{
            "featureType": "poi.park",
            "elementType": "geometry.fill",
            "stylers": [
		{
                    "color": "#b3ebcb"
		}
            ]
	},
	{
            "featureType": "landscape.natural",
            "elementType": "geometry.fill",
            "stylers": [
		{
                    "color": "#2be7f0"
		},
		{
                    "saturation": 57
		},
		{
                    "lightness": 90
		},
		{
                    "gamma": 1.77
		}
            ]
	},
	{
            "featureType": "poi",
            "elementType": "labels.icon",
            "stylers": [
		{
                    "visibility": "simplified"
		},
		{
                    "hue": "#2b7ff0"
		},
		{
                    "saturation": 20
		},
		{
                    "lightness": -8
		}
            ]
	},
	{
            "featureType": "transit",
            "elementType": "labels.icon",
            "stylers": [
		{
                    "hue": "#2b7ff0"
		},
		{
                    "saturation": -20
		},
		{
                    "lightness": 26
		}
            ]
	},
	{
            "featureType": "poi",
            "elementType": "geometry.fill",
            "stylers": [
		{
                    "color": "#b3ebcb"
		}
            ]
	},
	{
            "featureType": "poi.school",
            "elementType": "geometry.fill",
            "stylers": [
		{
                    "visibility": "off"
		},
		{
                    "color": "#2948e6"
		},
		{
                    "hue": "#2948e6"
		},
		{
                    "saturation": -50
		},
		{
                    "lightness": 36
		},
		{
                    "gamma": 2.49
		}
            ]
	},
	{
            "featureType": "water",
            "elementType": "geometry.fill",
            "stylers": [
		{
                    "color": "#33a5d9"
		},
		{
                    "saturation": -12
		},
		{
                    "lightness": 20
		}
            ]
	},
	{
            "featureType": "water",
            "elementType": "labels.text.fill",
            "stylers": [
		{
                    "color": "#121212"
		},
		{
                    "hue": "#000000"
		},
		{
                    "lightness": 27
		}
            ]
	},
	{
            "featureType": "road.highway",
            "elementType": "geometry.stroke",
            "stylers": [
		{
                    "visibility": "on"
		},
		{
                    "color": "#ffffff"
		}
            ]
	},
	{
            "featureType": "road.highway",
            "elementType": "geometry.fill",
            "stylers": [
		{
                    "color": "#0e4ea4"
		},
		{
                    "saturation": -20
		},
		{
                    "lightness": 45
		},
		{
                    "gamma": 2.42
		}
            ]
	}
    ];

    var map_style = new google.maps.StyledMapType(map_style_definition,
						  {name: 'GeoWeb Style'});
    
    map = new google.maps.Map(document.getElementById('map'), {
	// @TODO: Somehow fetch center of SAM and center map there.
	//        Remove this static values.
        center: {lat: -33.71108463, lng: 151.01125614},
        zoom: 15
    });

    map.mapTypes.set('styled_map', map_style);
    map.setMapTypeId('styled_map');
    
    // Load SAM list
    $scope.available_sams = []
    $http.get('/api/stats/sam').then(function(resp){
	if (resp.data.status == 'OK'){
	    $scope.available_sams = resp.data.data;
	} else {
	    $scope.errors = resp.data.errors;
	}
    }, function(resp){
	$scope.errors = ['Could not fetch SAM list!'];
    });

    $scope.load_sam = function(sam){

	// coaxialCable
	// @TODO: Make a generic function to load any layer.
	//        Make sure data from API is self descriptive and generic
	$http.get('/api/layer/' + sam + '/coaxialCable').then(function(resp) {

	    data = resp.data;
	    element_type = data.element;
	    elements = data.data;

	    // @TODO: Save each instance of polyline in an array
	    //        for future manipulation
	    //        Change the iteration to make more effective
	    for(var i = 0; i < elements.length; i ++){
		// render each cable
		var cable_coordinates_raw = elements[i].posList.split(' ');
		var cable_coordinates = [];
		for (var c = 0; c < cable_coordinates_raw.length; c ++){
		    cable_coordinates[cable_coordinates.length] = {
			lat: parseFloat(cable_coordinates_raw[c++]),
			lng: parseFloat(cable_coordinates_raw[c])
		    };
		}
		console.log(cable_coordinates);
		var cable_polyline = new google.maps.Polyline({
		    path: cable_coordinates,
		    geodesic: true,
		    strokeColor: '#1982D1',
		    strokeOpacity: 1.0,
		    strokeWeight: 3
		});
		cable_polyline.setMap(map);
	    }
	    
	}, function(resp){
	    $scope.errors = ['Could not fetch coaxialCable layer!'];
	});
	
    };
    
}]);
