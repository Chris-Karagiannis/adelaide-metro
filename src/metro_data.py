from google.transit import gtfs_realtime_pb2
import requests, zipfile, io, csv, os.path
import sqlite3

class MetroData:
    def __init__(self, root_path):
        self.root_path = root_path

    # Checks for new version
    def new_version(self):       
        version = requests.get('https://gtfs.adelaidemetro.com.au/v1/static/latest/version.txt').json()
        
        feed_version = -1

        if os.path.isfile(self.root_path + '/data/feed_info.txt'):
            with open(self.root_path + '/data/feed_info.txt', newline='') as csvfile:
                for row in csv.DictReader(csvfile):
                    feed_version = int(row['feed_version'])
        
        return feed_version != version

    
    # Update if new versions do not match
    def update_data(self):    
        if self.new_version():
            response = requests.get('https://gtfs.adelaidemetro.com.au/v1/static/latest/google_transit.zip')
            zip = zipfile.ZipFile(io.BytesIO(response.content))
            zip.extractall(self.root_path + '/data/')
            self.update_routes()
            self.update_shapes()
            self.update_trips()
            self.update_stops()
            self.update_stop_times()

    # Update vehicle positions
    def update_vehicles(self):
        url = 'https://gtfs.adelaidemetro.com.au/v1/realtime/vehicle_positions'
        feed = gtfs_realtime_pb2.FeedMessage()
        response = requests.get(url)
        feed.ParseFromString(response.content)

        vehicles = []

        for entity in feed.entity:
            if entity.HasField('vehicle'):
                vehicle = {
                    "trip_id" : entity.vehicle.trip.trip_id,
                    "route_id" : entity.vehicle.trip.route_id,
                    "latitude" : entity.vehicle.position.latitude,
                    "longitude" : entity.vehicle.position.longitude,
                    "timestamp" : entity.vehicle.timestamp,
                    "bearing" : entity.vehicle.position.bearing
                }

                vehicles.append(vehicle)
        
        return vehicles

    def update_routes(self):
        conn = sqlite3.connect('adel-metro.db')

        conn.execute("DELETE FROM Routes")

        sql =   "INSERT INTO Routes (RouteID, Name, Description, Colour) " \
                "VALUES (?, ?, ?, ?) "
                
        with open(self.root_path + '/data/routes.txt', newline='') as csvfile:
            for row in csv.DictReader(csvfile):
                conn.execute(sql, (row['route_id'], row['route_long_name'], row['route_desc'], row['route_color']))
        
        conn.commit()
        conn.close()
    
    def update_trips(self):
        conn = sqlite3.connect('adel-metro.db')
        conn.execute("DELETE FROM Trips")

        sql =   "INSERT INTO Trips (TripID, RouteID, ShapeID) " \
                "VALUES (?, ?, ?) "
        
        with open(self.root_path + '/data/trips.txt', newline='') as csvfile:
            for row in csv.DictReader(csvfile):
                conn.execute(sql, (row['trip_id'], row['route_id'], row['shape_id']))
            
        conn.commit()
        conn.close()

    def update_shapes(self):
        conn = sqlite3.connect('adel-metro.db')
        conn.execute("DELETE FROM Shapes")

        sql =   "INSERT INTO Shapes (ShapeID, ShapeSeqNo, Latitude, Longitude, DistanceTraveled) " \
                "VALUES (?, ?, ?, ?, ?) "
        
        with open(self.root_path + '/data/shapes.txt', newline='') as csvfile:
            for row in csv.DictReader(csvfile):
                conn.execute(sql, (row['shape_id'], row['shape_pt_sequence'], row['shape_pt_lat'], row['shape_pt_lon'], row['shape_dist_traveled']))
            
        conn.commit()
        conn.close()

    def update_stops(self):
        conn = sqlite3.connect('adel-metro.db')
        conn.execute("DELETE FROM Stops")

        sql =   "INSERT INTO Stops (StopID, StopName, StopDescription, Latitude, Longitude, Url) " \
                "VALUES (?, ?, ?, ?, ?, ?) "
        
        with open(self.root_path + '/data/stops.txt', newline='') as csvfile:
            for row in csv.DictReader(csvfile):
                conn.execute(sql, (row['stop_id'], row['stop_name'], row['stop_desc'], row['stop_lat'], row['stop_lon'], row['stop_url']))

        conn.commit()
        conn.close()

    def update_stop_times(self):
        conn = sqlite3.connect('adel-metro.db')
        conn.execute("DELETE FROM StopTimes")

        sql =   "INSERT INTO StopTimes (StopID, TripID, ArrivalTime, DepartureTime) " \
                "VALUES (?, ?, ?, ?) "
        
        with open(self.root_path + '/data/stop_times.txt', newline='') as csvfile:
            for row in csv.DictReader(csvfile):
                conn.execute(sql, (row['stop_id'], row['trip_id'], row['arrival_time'], row['departure_time']))

        conn.commit()
        conn.close()