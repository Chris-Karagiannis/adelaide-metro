from google.transit import gtfs_realtime_pb2
import requests
import csv
import os

url = 'https://gtfs.adelaidemetro.com.au/v1/realtime/vehicle_positions'

def get_route_data(root_path):
    data = {}

    with open(root_path + '/services/data/routes.txt', newline='') as csvfile:
        for row in csv.DictReader(csvfile):
            data[row['route_id']] = {
                'name': row['route_long_name'],
                'description':row['route_desc'],
                'colour': row['route_color']
            }
    
    return data


def fetch_transport_data(root_path):
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get(url)
    feed.ParseFromString(response.content)
    print(feed)
    data = {"vehicles":[]}
    route_data = get_route_data(root_path)

    for entity in feed.entity:
        if entity.HasField('vehicle'):
            data["vehicles"].append({
                "route": entity.vehicle.trip.route_id,
                "route_data": route_data[entity.vehicle.trip.route_id],
                "latitude": entity.vehicle.position.latitude, 
                "longitude": entity.vehicle.position.longitude,
                "time": entity.vehicle.timestamp,
                "trip_id": entity.vehicle.trip.trip_id,
                "bearing": entity.vehicle.position.bearing
            })
                    

    return data

