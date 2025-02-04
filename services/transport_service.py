from google.transit import gtfs_realtime_pb2
import requests, zipfile, io, csv, os.path

def update_data(root_path):

    # Only update if there is a version change
    version = requests.get('https://gtfs.adelaidemetro.com.au/v1/static/latest/version.txt').json()
    feed_version = -1
    
    # Check if the file exists before trying to open to avoid errors
    if os.path.isfile(root_path + '/services/data/feed_info.txt'):
        with open(root_path + '/services/data/feed_info.txt', newline='') as csvfile:
            for row in csv.DictReader(csvfile):
                feed_version = int(row['feed_version'])

    # Get new data if version numbers do not match
    if feed_version != version:
        response = requests.get('https://gtfs.adelaidemetro.com.au/v1/static/latest/google_transit.zip')
        zip = zipfile.ZipFile(io.BytesIO(response.content))
        zip.extractall(root_path + '/services/data/')

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
    url = 'https://gtfs.adelaidemetro.com.au/v1/realtime/vehicle_positions'
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get(url)
    feed.ParseFromString(response.content)
    data = {
        "vehicles":[]
    }

    update_data(root_path)
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


