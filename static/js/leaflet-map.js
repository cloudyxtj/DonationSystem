document.addEventListener("DOMContentLoaded", function () {
    const mapDataEl = document.getElementById("map-coords");
    const mapContainer = document.getElementById("map");

    if (!mapDataEl || !mapContainer) return;

    try {
        const mapData = JSON.parse(mapDataEl.textContent);
        const bounds = [];
        const map = L.map('map');

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(map);

        // Add pickup marker
        if (mapData.pickup?.lat !== null && mapData.pickup?.lng !== null) {
            const pickupLatLng = [mapData.pickup.lat, mapData.pickup.lng];
            L.marker(pickupLatLng)
                .addTo(map)
                .bindPopup(`<strong>${mapData.pickup.label}</strong><br>${mapData.pickup.address}`);
            bounds.push(pickupLatLng);
        }

        // Add delivery marker
        if (mapData.delivery?.lat !== null && mapData.delivery?.lng !== null) {
            const deliveryLatLng = [mapData.delivery.lat, mapData.delivery.lng];
            L.marker(deliveryLatLng)
                .addTo(map)
                .bindPopup(`<strong>${mapData.delivery.label}</strong><br>${mapData.delivery.address}`);
            bounds.push(deliveryLatLng);
        }

        // Draw polyline if both points exist
        if (bounds.length === 2) {
            L.polyline(bounds, { color: 'blue', weight: 4 }).addTo(map);
        }

        // Fit map to bounds
        if (bounds.length > 0) {
            map.fitBounds(bounds, { padding: [50, 50] });
        } else {
            mapContainer.innerHTML = "<p class='text-muted'>Location not available</p>";
        }
    } catch (error) {
        console.error("Map JSON parsing error:", error);
        mapContainer.innerHTML = "<p class='text-danger'>Error loading map</p>";
    }
});
