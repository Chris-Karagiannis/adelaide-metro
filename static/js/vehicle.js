export class Vehicle {
    constructor(tripID, routeID, route, latitude, longitude, bearing, timestamp, layer) {
        this.tripID = tripID
        this.routeID = routeID
        this.route = route
        this.latitude = latitude
        this.longitude = longitude
        this.bearing = bearing
        this.date = new Date(timestamp * 1000)
        this.layer = layer
        this.marker = this.createMarker()
    }

    createMarker() {
        const marker = L.marker([this.latitude, this.longitude], {
            icon: new L.DivIcon({
                iconSize: [40, 40],
                className: "marker-container",
                html: `<i class="fa fa-circle fa-2x marker" aria-hidden="true" style="color:#${this.route.colour};"></i>
                    <i class="fa fa-circle-o fa-2x marker" aria-hidden="true"></i>
                    <i class="fa fa-arrow-up marker" style="color:white; transform: rotate(${this.bearing}deg)" aria-hidden="true"></i>`
            })
        }).addTo(this.layer)

        marker.setZIndexOffset(200)

        marker.bindTooltip(`
                <b class="tooltip-route" style="background-color:#${this.route.colour};">${this.routeID}</b>
                <br>
                ${this.date.toLocaleString('en-AU')}
            `);

        marker.on('click', (e) => {
            this.layer.eachLayer(layer => {
                layer !== this.marker ? layer._icon.classList.add('hide') : layer._icon.classList.remove('hide');
            })
        })

        return marker
    }

}
