import csv

def trip_id_to_shape_id(root_path, trip_id):
    with open(root_path + '/services/data/trips.txt', newline='') as csvfile:
        for row in csv.DictReader(csvfile):
            if row['trip_id'] == trip_id:
                return row['shape_id']
    
    return -1

def get_stop_data(root_path):
    trip_data = {}
    stop_data = {}

    # Add trip ids to dict
    with open(root_path + '/services/data/stop_times.txt', newline='') as csvfile:
        for row in csv.DictReader(csvfile):
            if row['trip_id'] not in trip_data:
                trip_data[row['trip_id']] = []
            else:
                trip_data[row['trip_id']].append(row['stop_id'])
    # Get stops
    with open(root_path + '/services/data/stops.txt', newline='') as csvfile:
        for row in csv.DictReader(csvfile):
            stop_data[row['stop_id']] = {
                "name": row['stop_name'],
                "lat": row['stop_lat'],
                "lon": row['stop_lon'],
                "desc": row['stop_desc']
            }
            
    return {
        "trip_data":trip_data, 
        "stop_data":stop_data
    }

    

def get_shape_data(root_path, trip_id, stop_data):

    shape_id = trip_id_to_shape_id(root_path, trip_id)

    data = {
        "shape": [],
        "stops": stop_data
    }

    with open(root_path + '/services/data/shapes.txt', newline='') as csvfile:
        for row in csv.DictReader(csvfile):
            if row['shape_id'] == shape_id:
                data['shape'].append([row['shape_pt_lat'], row['shape_pt_lon']])               
    
    return data
