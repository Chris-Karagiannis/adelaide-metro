import csv

def trip_id_to_shape_id(root_path, trip_id):
    with open(root_path + '/services/data/trips.txt', newline='') as csvfile:
        for row in csv.DictReader(csvfile):
            if row['trip_id'] == trip_id:
                return row['shape_id']
    
    return -1

def get_trip_data(root_path):
    trip_data = {}

    # Add trip ids to dict
    with open(root_path + '/services/data/stop_times.txt', newline='') as csvfile:
        for row in csv.DictReader(csvfile):
            if row['trip_id'] not in trip_data:
                trip_data[row['trip_id']] = []
            else:
                trip_data[row['trip_id']].append(row['stop_id'])
            
    return trip_data
   
def get_shape_data(root_path):
    shape_data = {}

    with open(root_path + '/services/data/shapes.txt', newline='') as csvfile:
        for row in csv.DictReader(csvfile):
            if row['shape_id'] not in shape_data:
                shape_data[row['shape_id']] = []
            else:
                shape_data[row['shape_id']].append([row['shape_pt_lat'], row['shape_pt_lon']])
    
    return shape_data

def fetch_shape_data(root_path, trip_id, trip_data, shape_data):
    shape_id = trip_id_to_shape_id(root_path, trip_id)

    data = {
        "shape": shape_data[shape_id],
        "stops": trip_data[trip_id]
    }        
    
    return data
