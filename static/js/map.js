// map.js

function initMap(spots, defaultLat = 18.5204, defaultLng = 73.8567) {
    // Initialize map
    var map = L.map('map').setView([defaultLat, defaultLng], 12);

    // Add OpenStreetMap layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Add markers for each spot
    spots.forEach(function(spot) {
        if (spot.lat && spot.lng) {
            var marker = L.marker([spot.lat, spot.lng]).addTo(map);
            marker.bindPopup(
                "<b>" + spot.location + "</b><br>" +
                "₹" + spot.price + "/hr<br>" +
                "Timings: " + spot.timings + "<br>" +
                (spot.available ? "<span style='color:green;'>Available</span>" : "<span style='color:red;'>Not Available</span>")
            );
        }
    });
}
