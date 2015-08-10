//
// Global variables
//

var map;
var activeMap = null;
var buildingMap;
var boston = new google.maps.LatLng(42.3601, -71.0589);

//
// Data loaded from backend
//

var buildingMapData  = [
  {location: new google.maps.LatLng(37.782, -122.447), weight: 0.5},
  new google.maps.LatLng(37.782, -122.445),
  {location: new google.maps.LatLng(37.782, -122.443), weight: 2},
  {location: new google.maps.LatLng(37.782, -122.441), weight: 3},
  {location: new google.maps.LatLng(37.782, -122.439), weight: 2},
  new google.maps.LatLng(37.782, -122.437),
  {location: new google.maps.LatLng(37.782, -122.435), weight: 0.5},

  {location: new google.maps.LatLng(37.785, -122.447), weight: 3},
  {location: new google.maps.LatLng(37.785, -122.445), weight: 2},
  new google.maps.LatLng(37.785, -122.443),
  {location: new google.maps.LatLng(37.785, -122.441), weight: 0.5},
  new google.maps.LatLng(37.785, -122.439),
  {location: new google.maps.LatLng(37.785, -122.437), weight: 2},
  {location: new google.maps.LatLng(37.785, -122.435), weight: 3}
];

//
// Data loading methods
//

//
// Heatmap utility methods
//

function makeHeatMap(heatMapData) {
  return new google.maps.visualization.HeatmapLayer({
    data: heatMapData,
});
}

function setHeatMapActive(heatMap) {
  if (activeMap != null ) {
    activeMap.setMap(null);
  }
  heatMap.setMap(map);
}

//
// Google maps UI
//

function Button(parentElement, text, functionCallback) {
  var button = document.createElement('a');
  button.className = 'btn btn-default btn-circle';
  button.innerHTML = text;
  parentElement.appendChild(button);

  var icon = document.createElement('span');
  icon.className = 'glyphicon glyphicon-search';
  button.appendChild(icon);

  google.maps.event.addDomListener(button, 'click', functionCallback);
}

function CenterControl(controlDiv, map) { 

  // Set CSS for the control border
  var controlUI = document.createElement('div');
  controlUI.style.backgroundColor = '#fff';
  controlUI.style.border = '2px solid #fff';
  controlUI.style.borderRadius = '3px';
  controlUI.style.boxShadow = '0 2px 6px rgba(0,0,0,.3)';
  controlUI.style.cursor = 'pointer';
  controlUI.style.marginBottom = '22px';
  controlUI.style.textAlign = 'center';
  controlUI.title = 'Click to recenter the map';
  controlUI.style.width = '200px';

  controlDiv.appendChild(controlUI);

  Button(controlUI, 'Center ', function() {
      map.setCenter(boston);
  });

  Button(controlUI, 'Building Permits ', function() {
      buildingMap.setMap(map);
  });
  
/*
  // Set CSS for the control interior
  var controlText = document.createElement('div');
  controlText.style.color = 'rgb(25,25,25)';
  controlText.style.fontFamily = 'Roboto,Arial,sans-serif';
  controlText.style.fontSize = '16px';
  controlText.style.lineHeight = '38px';
  controlText.style.paddingLeft = '5px';
  controlText.style.paddingRight = '5px';
  controlText.innerHTML = 'Center Map';
  controlUI.appendChild(controlText);

  // Setup the click event listeners: simply set the map to
  // Chicago
  google.maps.event.addDomListener(controlUI, 'click', function() {
    map.setCenter(boston)
  });*/
}

//
// Initialize Method
//

function initialize() {
  var mapDiv = document.getElementById('map-canvas');
  var mapOptions = {
    zoom: 12,
    center: boston, //new google.maps.LatLng(42.3601, -71.0589), // 42.3601° N, 71.0589° W
    mapTypeControl: false,
  }
  map = new google.maps.Map(mapDiv, mapOptions);

  var centerControlDiv = document.createElement('div');
  var centerControl = new CenterControl(centerControlDiv, map);

  centerControlDiv.index = 1;
  map.controls[google.maps.ControlPosition.TOP_RIGHT].push(centerControlDiv);

  buildingMap = makeHeatMap(buildingMapData);
  setHeatMapActive(buildingMap);
}

//
// Actual code called
//

google.maps.event.addDomListener(window, 'load', initialize);
