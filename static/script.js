// Centre map on Adelaide
const map = L.map('map', {
    center: [-34.9285, 138.6007],
    zoom: 10,
});

// Add markers to map for vehicles
for (let i = 0; i < transportData.vehicles.length; i++) {
    const vehicle = L.marker([transportData.vehicles[i].latitude, transportData.vehicles[i].longitude]).addTo(map);
    const date = new Date(transportData.vehicles[i].time * 1000)
    vehicle.bindPopup(`<strong>Route:</strong> ${transportData.vehicles[i].route}<br><sub>${date.toLocaleString('en-AU')}</sub>`)
}

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    minZoom: 9,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);
