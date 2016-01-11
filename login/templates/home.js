function initialize() {
  		var mapCanvas = document.getElementById('map');
  		var mapOptions = {
    			center: new google.maps.LatLng({{new_location_text}}),
    			zoom: 13,
    			mapTypeId: google.maps.MapTypeId.ROADMAP,
    			disableDefaultUI: true,
  		}
  		var map = new google.maps.Map(mapCanvas, mapOptions)
		}
		google.maps.event.addDomListener(window, 'load', initialize);