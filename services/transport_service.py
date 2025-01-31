from google.transit import gtfs_realtime_pb2
import requests

url = 'https://gtfs.adelaidemetro.com.au/v1/realtime/vehicle_positions'

def fetch_transport_data():
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get(url)
    feed.ParseFromString(response.content)

    data = {"vehicles":[]}

    for entity in feed.entity:
        if entity.HasField('vehicle'):
            data["vehicles"].append({
                "route": entity.vehicle.trip.route_id,
                "latitude": entity.vehicle.position.latitude, 
                "longitude": entity.vehicle.position.longitude,
                "time": entity.vehicle.timestamp,
                "trip_id": entity.vehicle.trip.trip_id
            })
                    

    return data

