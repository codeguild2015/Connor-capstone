
function initialize() {
        "{% if markers %}"
        var markers = "{{markers |safe}}";
        "{% else %}"
        var markers = [];
        "{% endif %}"
            var mapCanvas = document.getElementById('map');
            var mapOptions = {
                zoom: "{{zoom}}",
                mapTypeId: google.maps.MapTypeId.ROADMAP,
                disableDefaultUI: true,
            }
            var map = new google.maps.Map(mapCanvas, mapOptions)
            map.setCenter(new google.maps.LatLng("{{new_location_text}}"))
            for(i = 0; i < markers.length; i++) {
              var position = new google.maps.LatLng(markers[i][0], markers[i][1]);
              var marker = new google.maps.Marker({
                position: position,
                map: map,
                icon: markers[i][3],
              })
            }
          }
google.maps.event.addDomListener(window, 'load', initialize);
