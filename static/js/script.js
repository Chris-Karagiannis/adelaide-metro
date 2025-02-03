// Centre map on Adelaide
const lat = localStorage.getItem('lat') ? localStorage.getItem('lat') : -34.9285;
const lng = localStorage.getItem('lng') ? localStorage.getItem('lng') : 138.6007;
const zoom = localStorage.getItem('zoom') ? localStorage.getItem('zoom') : 10;

const map = L.map('map', {
    center: [lat, lng],
    zoom: zoom,
});

// Store position and zoom in localstorage
map.on('zoomend', (e) => {
    localStorage.setItem('zoom', map.getZoom())
})

map.on('moveend', (e) => {
    localStorage.setItem('lat', map.getCenter().lat)
    localStorage.setItem('lng', map.getCenter().lng)
})

// Add markers to map for vehicles
for (let i = 0; i < transportData.vehicles.length; i++) {
    const vehicle = L.marker([transportData.vehicles[i].latitude, transportData.vehicles[i].longitude], {
        icon: new L.DivIcon({
        iconSize: [40, 40],
        className: "marker-container",
        html: `<i class="fa fa-circle fa-2x marker" id="${i}" aria-hidden="true"></i>
               <i class="fa fa-arrow-up marker" style="color:white; transform: rotate(${transportData.vehicles[i].bearing}deg)" id="${i}" aria-hidden="true"></i>`
    })}).addTo(map);

    // Set colour of vehicle per route data
    document.getElementById(i).style.color = `#${transportData.vehicles[i].route_data.colour}`
    
    const date = new Date(transportData.vehicles[i].time * 1000)

    // Marker popup with info
    vehicle.bindTooltip(`
        <strong class="tooltip-route" style="background-color:#${transportData.vehicles[i].route_data.colour};">${transportData.vehicles[i].route}</strong> ${transportData.vehicles[i].route_data.name}
        <br>
        <sub>${date.toLocaleString('en-AU')}</sub>
    `)

    // Click event
    vehicle.on('click', (e) => {
        map.setView(e.latlng, 16);
    })
}

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    minZoom: 9,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);
