//
// Global variables
//

var map;
var activeMap = null;
var boston = new google.maps.LatLng(42.3601, -71.0589);

//
// Loads data from database
//

var dummyData = "37.782:-122.447;" +
                "37.78:-122.445;"  +
                "37.782:-122.443;" +
                "37.782:-122.441;" +
                "37.782:-122.439;" +
                "37.782:-122.437;" +
                "37.782:-122.435;" + 
                "37.785:-122.447;" +
                "37.785:-122.445;" +
                "37.785:-122.443;" +
                "37.785:-122.441;" + 
                "37.785:-122.439;" +
                "37.785:-122.437;" +
                "37.785:-122.435;";

function loadHMData(str_data) {
  console.log(str_data);
  pairs = str_data.split(';');
  console.log(pairs);
  result = [];
  for (var i = 0, len = pairs.length; i < len; i++) {
    if (pairs[i].length != 0) {
      lat_lng = pairs[i].split(':');
      console.log(lat_lng);
      result.push(new google.maps.LatLng(parseFloat(lat_lng[0]),
                                         parseFloat(lat_lng[1])));
    }
  }
  return result;
}

var buildingMap = new google.maps.visualization.HeatmapLayer({
  data: loadHMData(dummyData),
});

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

  
  // Recenter Button
  google.maps.event.addDomListener(controlUI, 'click', function() {
    map.setCenter(boston)
  });

  // Show Building Permits
  Button(controlUI, 'Building Permits ', function() {
    buildingMap.setMap(buildingMap.getMap() ? null : map);
  });
}

//
// Initialize Method
//

function initialize() {
  // Caputre map div
  var mapDiv = document.getElementById('map-canvas');
  var mapOptions = {
    zoom: 12,
    center: boston, // 42.3601° N, 71.0589° W
    mapTypeControl: false,
  }
  map = new google.maps.Map(mapDiv, mapOptions);

  var centerControlDiv = document.createElement('div');
  var centerControl = new CenterControl(centerControlDiv, map);

  centerControlDiv.index = 1;
  map.controls[google.maps.ControlPosition.TOP_RIGHT].push(centerControlDiv);

  setHeatMapActive(buildingMap);
}

//
// Actual code called
//

google.maps.event.addDomListener(window, 'load', initialize);
