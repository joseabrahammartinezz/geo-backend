//vista amplia del mapa
var mapId = document.getElementById('map');
function fullScreenView(){
    if(document.fullscreenElement){
        document.exitFullscreen();
    }
    else {
        mapId.requestFullscreen();
    }
    
};

/*//imprimir
$(".print-map").click(function () {
    window.print();
  });*/
 
 // L.control.browserPrint().addTo(map);
 L.control.browserPrint({position: 'topright', title: 'Imprimir', printModes: [
         L.BrowserPrint.Mode.Landscape("Tabloid",{title: "Vertical"}),
         L.BrowserPrint.Mode.Landscape("",{title: "Horizontal"}),
         L.BrowserPrint.Mode.Auto("B4",{title: "Automático"}),
         L.BrowserPrint.Mode.Custom("B5",{title:"Seleccionar área"})
 ],}).addTo(map);

 //Busquedas leaftleft
 L.Control.geocoder().addTo(map);
 
 //medir distancias
 L.control.measure({ 
     primaryLengthUnit: 'meters', 
     secondaryLengthUnit: 'kilometers',
     primaryAreaUnit: 'sqmeters', 
     secondaryAreaUnit: undefined 
  }
 ).addTo(map);

//zoom de capa
$(".zoom-to-layer").click(function () {
    map.setView([-17.393876179376512,-66.18222116754181], 13);
  })