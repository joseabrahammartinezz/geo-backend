//inicializando clase map
var map = L.map('map').setView([-17.393876179376512,-66.18222116754181], 13);
map.zoomControl.setPosition('topright');

//adicionando capa
var osm= L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

var OpenTopoMap = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
    maxZoom: 17,
    attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
});

var Stamen_TonerLite = L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/toner-lite/{z}/{x}/{y}{r}.{ext}', {
    attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    subdomains: 'abcd',
    minZoom: 0,
    maxZoom: 20,
    ext: 'png'
});

//colocando marcado al centro del mapa
var singleMarker =L.marker([-17.393876179376512,-66.18222116754181])
    .bindPopup('A pretty CSS3 popup.<br> Easily customizable.')
    .openPopup();

//aumentando escala
L.control.scale({position: 'bottomright'}).addTo(map);

//mostrar coordenadas
map.on("mousemove", function (e) {
    //console.log(e);
    $(".coordinate").html(`Lat: ${e.latlng.lat} Long: ${e.latlng.lng}`);
});



//GEojson
var marker = L.markerClusterGroup();
var taji= L.geoJSON(data,{
    onEachFeature: function (feature, layer){
        layer.bindPopup(feature.geometry.coordinates[0].toString() + " " + feature.geometry.coordinates[1].toString());
    }
});
taji.addTo(marker);
marker.addTo(map);



// Capas base
var baseMaps = {
    'OSM' : osm,
    'Mapa topográfico' : OpenTopoMap,
    'Stamen TonerLite' : Stamen_TonerLite
};

var overlayMaps ={
    'Puntos Geoson': marker,
    'Marcador Inicial' : singleMarker
};
L.control.layers(baseMaps,overlayMaps,{collapsed: false, position: "topleft"}).addTo(map);

