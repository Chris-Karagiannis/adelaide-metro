import csv

def trip_id_to_shape_id(root_path, trip_id):
    with open(root_path + '/services/data/trips.txt', newline='') as csvfile:
        for row in csv.DictReader(csvfile):
            if row['trip_id'] == trip_id:
                return row['shape_id']
    
    return -1

def get_shape_data(root_path, trip_id):

    shape_id = trip_id_to_shape_id(root_path, trip_id)

    data = []

    with open(root_path + '/services/data/shapes.txt', newline='') as csvfile:
        for row in csv.DictReader(csvfile):
            if row['shape_id'] == shape_id:
                data.append([row['shape_pt_lat'], row['shape_pt_lon']])               
    
    return data
