async function fetchData() {
    try {
        let response = await fetch('/api/data');
        let data = await response.json();
        processData(data)
    } catch (error) {
        console.error("Error fetching data:", error);
    }
}

async function fetchShape(tripID, colour) {
    try {
        let response = await fetch(`/api/shapes/${tripID}`);
        let data = await response.json();
        processShapes(data, colour)
    } catch (error) {
        console.error("Error fetching data:", error);
    }
}

function processData(transportData) {

    // Clear previous markers
    map.eachLayer(layer => {
        if (layer instanceof L.Marker && layer !== selected.marker) {
            map.removeLayer(layer);
        }
    });

    // Add markers to map for vehicles
    for (let i = 0; i < transportData.vehicles.length; i++) {

        // Add marker for vehicle
        const vehicle = L.marker([transportData.vehicles[i].latitude, transportData.vehicles[i].longitude], {
            icon: new L.DivIcon({
            iconSize: [40, 40],
            className: "marker-container",
            html: `<i class="fa fa-circle fa-2x marker" id="${i}" aria-hidden="true"></i>
                    <i class="fa fa-arrow-up marker" style="color:white; transform: rotate(${transportData.vehicles[i].bearing}deg)" id="${i}" aria-hidden="true"></i>`
        })}).addTo(map);

        // Set colour of vehicle per route data
        document.getElementById(i).style.color = `#${transportData.vehicles[i].route_data.colour}`
        
        // Get date and time of last update of vehicle
        const date = new Date(transportData.vehicles[i].time * 1000)

        // Marker popup with info
        vehicle.bindTooltip(`
            <strong class="tooltip-route" style="background-color:#${transportData.vehicles[i].route_data.colour};">${transportData.vehicles[i].route}</strong> ${transportData.vehicles[i].route_data.name}
            <br>
            <sub>${date.toLocaleString('en-AU')}</sub>
        `)

        // Marker popup with info
        vehicle.bindPopup(`
            <strong class="tooltip-route" style="background-color:#${transportData.vehicles[i].route_data.colour};">${transportData.vehicles[i].route}</strong> ${transportData.vehicles[i].route_data.name}
            <br>
            <sub>${date.toLocaleString('en-AU')}</sub>
        `)
        
        if (selected.tripID == transportData.vehicles[i].trip_id) {
            vehicle.openPopup()
        }

        // Click event
        vehicle.on('click', (e) => {
            
            // Vehicle path
            selected.tripID = transportData.vehicles[i].trip_id
            fetchShape(transportData.vehicles[i].trip_id, transportData.vehicles[i])
        })
               
    }
}

let selected = {
    tripID: undefined,
    line: undefined,
}

function adjust(color, amount) {
    return '#' + color.replace(/^#/, '').replace(/../g, color => ('0'+Math.min(255, Math.max(0, parseInt(color, 16) + amount)).toString(16)).substr(-2));
}

function processShapes(shape_data, vehicle_data) {
    if (selected.line !== undefined){
        map.removeLayer(selected.line);
    }

    const colour = adjust(`${vehicle_data.route_data.colour}`, 50)

    selected.line = L.polyline(shape_data, {
        color: colour,
        opacity: 1,
        weight: 8 
    }).addTo(map);

}

// Fetch vehicle data
fetchData();

// Fetch every 20 seconds
setInterval(fetchData, 20000)

// Refresh button
const refreshButton = document.getElementById("refreshButton")

refreshButton.addEventListener('click', () => {
    fetchData();
})

// Centre map on Adelaide or get previous position from local storage
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

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    minZoom: 9,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);
