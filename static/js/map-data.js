import { Vehicle } from "./vehicle.js";

export class MapData {
    constructor() {
        this.map = this.createMap();
        this.selected = null;
        this.routes = null;
        this.path = null;
        this.vehicles = L.layerGroup().addTo(this.map);
        this.stops = L.layerGroup().addTo(this.map);
        this.fetch();
        setInterval(this.fetch.bind(this), 5000);
    }

    async fetch() {
        try {
            const vehiclesResponse = await fetch('/api/vehicles');
            const vehicles = await vehiclesResponse.json();
            const routesResponse = await fetch('/api/routes');
            this.routes = await routesResponse.json();
            this.createVehicles(vehicles);
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    }

    createMap() {
        const map = L.map('map', {
            center: [-34.9285, 138.6007],
            zoom: 10,
        });

        map.on('click', (e) => {
            // Reset path, stops and vehicle markers
            this.vehicles.eachLayer(layer => {
                layer._icon.classList.remove('hide');               
            })
            this.stops.clearLayers()               
            this.path !== null ? this.path.removeFrom(this.map) : null
            this.selected = null;          
        })

        return map

    }

    createVehicles(vehicles) {
        this.vehicles.clearLayers()
        vehicles.forEach(vehicle => {
            const vehicleInstance = new Vehicle(vehicle.trip_id, vehicle.route_id, this.routes[vehicle.route_id], vehicle.latitude, vehicle.longitude, vehicle.bearing, vehicle.timestamp, this.vehicles)
            vehicleInstance.marker.on('click', (e) => {
                this.selected = vehicleInstance.tripID;
                this.createPath(vehicle.trip_id);
                this.createStops(vehicle.trip_id);
            })
            if (this.selected !== vehicleInstance.tripID && this.selected !== null){
                vehicleInstance.marker._icon.classList.add('hide')
            }
        });
    }

    async createPath(tripID) {
        try {
            // Create Path from shape data
            const shapeResponse = await fetch(`/api/shapes/${tripID}`);
            const shapeData = await shapeResponse.json();

            // Get rid of previous path if it exists
            if (this.path !== null) {
                this.path.removeFrom(this.map)
            }

            this.path = L.polyline(shapeData, {
                color: '#de2d26',
                opacity: 1,
                weight: 3
            })
            .addTo(this.map);
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    }

    async createStops(tripID) {
        try {       
            // Add new stops
            const stopsResponse = await fetch(`/api/stops/${tripID}`);
            const stopsData = await stopsResponse.json();
    
            // Remove previous stops
            this.stops.eachLayer(layer => {
                layer.remove()
            })
    
            stopsData.forEach(stop => {
                const stopMarker = L.marker([stop.latitude, stop.longitude], {
                    icon: new L.DivIcon({
                        iconSize: [40, 40],
                        className: "marker-container",
                        html: `<i class="fa fa-circle marker" aria-hidden="true" style="color: white;"></i>
                               <i class="fa fa-circle-o marker" aria-hidden="true" ></i>`
                        })
                    })
                    .bindTooltip(`
                        <b>${stop.name}</b>
                        <br> 
                        Arrival Time: ${stop.arrivalTime}
                        <br>
                        Departure Time: ${stop.departureTime}
                    `)
                    .addTo(this.stops)
    
                stopMarker.setZIndexOffset(100)
            })
    
            this.path.bringToBack()
        } catch (error) {
            console.error("Error fetching data:", error);
        }        
    }
}