const copy =
  "&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a>";
const url =
  "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
const layer = L.tileLayer(url, {
  attribution: copy,
});
const map = L.map("map", {
  layers: [layer],
  minZoom: 5,
});
map
  .locate()
  .on("locationfound", (e) =>
    map.setView(e.latlng, 8)
  )
  .on("locationerror", () =>
    map.setView([0, 0], 5)
  )
;

var variable_id;
var geoJSONLayer = L.geoJSON().addTo(map);

$(document).ready(function() {  
  $('.form-select').change(function(){
    if (this.value != 0) {
      variable_id = this.value;
      geoJSONLayer.clearLayers();
      render_stations();
    } else {
      variable_id = null;
      geoJSONLayer.clearLayers();
      render_stations();
    }
  });
});

async function load_stations() {
  if (variable_id) {
    api_url = `/api/last_datas/?variable_id=${variable_id}&in_bbox=`
  } else {
    api_url = `/api/stations/?in_bbox=`
  }
  const stations_url = api_url + map.getBounds().toBBoxString();
  const response = await fetch(
    stations_url
  );
  const geojson = await response.json();
  return geojson;
}

async function render_stations() {
  const stations = await load_stations();
  geoJSONLayer.clearLayers();
  geoJSONLayer = L.geoJSON(stations.results, {
    pointToLayer: function(feature,latlng) {
      return L.marker(latlng);
    },
    onEachFeature: function(feature, layer) {
      //if (feature.properties.consuming == true) {
      //  layer.bindPopup(feature.properties.name + ", consuming...")
      //} else {
      console.log(feature);
      if (variable_id) {
        layer.bindPopup(feature.properties.station_name + "\n" + feature.properties.value + " " + feature.properties.unit_symbol)
      } else {
        layer.bindPopup(feature.properties.name);
      }
      layer.on('mouseover', function() { layer.openPopup(); })
      layer.on('mouseout', function() { layer.closePopup(); })
    }
  })
  .addTo(map);
}
  
map.on("moveend", render_stations);