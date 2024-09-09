document.addEventListener('DOMContentLoaded', function () {
    var map = L.map('map');
    var hospitals = [];
    var detailsPanel = document.getElementById('hospital-details');
    var userLat, userLng;
    var routeControl = L.Routing.control({
        waypoints: [],
        routeWhileDragging: true,
        createMarker: function() { return null; } // Do not show route markers
    }).addTo(map);

    // Define custom icons
    var userIcon = L.icon({
        iconUrl: 'https://static.vecteezy.com/system/resources/previews/017/178/337/non_2x/location-map-marker-icon-symbol-on-transparent-background-free-png.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [0, -41]
    });

    var hospitalIcon = L.icon({
        iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [0, -41]
    });

    function initMap(lat, lng) {
        userLat = lat;
        userLng = lng;

        map.setView([lat, lng],13);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: ''
        }).addTo(map);

        L.marker([lat, lng], {icon: userIcon}).addTo(map)
            .bindPopup('Your Location')
            .openPopup();

        fetchHospitals(lat, lng);
    }

    function fetchHospitals(lat, lng) {
        var radius = 5000;  // Radius in meters
        var overpassUrl = `http://overpass-api.de/api/interpreter?data=[out:json];(node["amenity"="hospital"](around:${radius},${lat},${lng}););out body;`;

        fetch(overpassUrl)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('API Response:', data);
                if (data.elements) {
                    hospitals = data.elements.map(element => ({
                        name: element.tags.name || 'Unnamed',
                        address: (element.tags['addr:full'] || '') + ' ' + (element.tags['addr:district'] || '') + ' ' + (element.tags['addr:postcode'] || ''),
                        latitude: element.lat,
                        longitude: element.lon,
                        website: element.tags.website || 'Not provided',
                        phone: element.tags['contact:phone'] || 'Not provided'
                    }));

                    // Sort hospitals by distance
                    hospitals.sort((a, b) => calculateDistance(userLat, userLng, a.latitude, a.longitude) - calculateDistance(userLat, userLng, b.latitude, b.longitude));

                    displayHospitals();
                } else {
                    console.error('No elements found in API response');
                }
            })
            .catch(error => {
                console.error('Fetch error:', error);
                alert('Error fetching hospital data. Please try again later.');
            });
    }

    function calculateDistance(lat1, lon1, lat2, lon2) {
        var R = 6371; // Radius of the earth in km
        var dLat = toRad(lat2 - lat1);
        var dLon = toRad(lon2 - lon1);
        var a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
                Math.sin(dLon / 2) * Math.sin(dLon / 2);
        var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        var d = R * c; // Distance in km
        return d * 1000; // Convert to meters
    }

    function toRad(deg) {
        return deg * (Math.PI / 180);
    }

    function displayHospitals() {
        detailsPanel.innerHTML = ''; // Clear previous details

        if (hospitals.length === 0) {
            detailsPanel.innerHTML += '<p>No hospitals found.</p>';
        } else {
            hospitals.forEach(hospital => {
                var markerPosition = [hospital.latitude, hospital.longitude];
                var marker = L.marker(markerPosition, {icon: hospitalIcon}).addTo(map);
                marker.bindPopup(
                    `<b>${hospital.name}</b><br>${hospital.address}<br>
                     Website: <a href="${hospital.website}" target="_blank">${hospital.website}</a><br>
                     Phone: ${hospital.phone}`
                );

                var div = document.createElement('div');
                div.className = 'hospital-item';
                div.innerHTML = `<b>${hospital.name}</b><br>${hospital.address}`;
                div.onclick = function() {
                    // Set the route from the user's location to the hospital
                    routeControl.setWaypoints([
                        L.latLng(userLat, userLng),
                        L.latLng(hospital.latitude, hospital.longitude)
                    ]);
                    map.setView(markerPosition, 14);
                    marker.openPopup();
                };
                detailsPanel.appendChild(div);
            });
        }
    }

    function filterHospitals(query) {
        var filteredHospitals = hospitals.filter(hospital => 
            hospital.name.toLowerCase().includes(query.toLowerCase()) ||
            hospital.address.toLowerCase().includes(query.toLowerCase())
        );
        displayHospitals(filteredHospitals);
    }

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var userLat = position.coords.latitude;
            var userLng = position.coords.longitude;
            initMap(userLat, userLng);
        }, function() {
            alert('Unable to retrieve your location.');
            initMap(51.505, -0.09);  // Fallback to a default location
        });
    } else {
        alert('Geolocation is not supported by this browser.');
        initMap(51.505, -0.09);  // Fallback to a default location
    }
});