// Initialize and add the map
function initMap() {
    var map;
    var bounds = new google.maps.LatLngBounds();
    var mapOptions = {
        mapTypeId: 'roadmap'
    };

    // Display a map on the web page
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
    map.setTilt(100);

    // Info window content generation function
    function getInfoWindowContent(marker) {
        return `
            <div class="info_content">
                
                <h2>${marker[3]}</h2>  
                <h3>Address : ${marker[0]}</h3>
                <h3>Capacity : ${marker[5]}</h3>
                <h3>Fee : ${marker[6]}</h3>
                <h3>Infrastrucure : ${marker[7]}</h3>
                <a class="home-btn" href="/homepage/navigate/${marker[1]}/${marker[2]}/${marker[3]}">Navigate</a>
                <a class="home-btn" href="/homepage/occupancyjuvisy/${marker[4]}">Occupancy</a>
            </div>
        `;
    }

    // Add multiple markers to map
    var infoWindow = new google.maps.InfoWindow(), marker, i;
    var allMarkers = [];


    // Place each marker on the map  
    for (i = 0; i < markers.length; i++) {
        var position = new google.maps.LatLng(markers[i][1], markers[i][2]);
        bounds.extend(position);
        marker = new google.maps.Marker({
            position: position,
            map: map,
            title: markers[i][3]
        });

        // Add marker to the array
        allMarkers.push(marker);

        // Add info window to marker    
        google.maps.event.addListener(marker, 'click', (function(marker, i) {
            return function() {
                infoWindow.setContent(getInfoWindowContent(markers[i]));
                infoWindow.open(map, marker);
            }
        })(marker, i));

        // Center the map to fit all markers on the screen
        map.fitBounds(bounds);
    }

    // Set zoom level
    var boundsListener = google.maps.event.addListener((map), 'bounds_changed', function(event) {
        this.setZoom(10);
        google.maps.event.removeListener(boundsListener);
    });

    // Store the map and all markers for later use
    window.map = map;
    window.allMarkers = allMarkers;
}

// Function to handle dropdown selection
function selectParkingLot() {
    var select = document.getElementById('parking-select');
    var value = select.value;

    if (value) {
        var latLng = value.split(',');
        var position = new google.maps.LatLng(latLng[0], latLng[1]);
        window.map.setCenter(position);
        window.map.setZoom(15);

        // Find the selected marker and trigger its click event
        for (var i = 0; i < window.allMarkers.length; i++) {
            var marker = window.allMarkers[i];
            if (marker.position.lat() == latLng[0] && marker.position.lng() == latLng[1]) {
                google.maps.event.trigger(marker, 'click');
                break;
            }
        }
    }
}
