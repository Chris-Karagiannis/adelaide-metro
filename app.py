from flask import Flask, render_template, jsonify
from src.metro_data import MetroData
import sqlite3

app = Flask(__name__)
data = MetroData(app.root_path)
data.update_data()

@app.route("/")
def index():
    return render_template("index.jinja")

@app.route("/api/vehicles")
def vehicles():
    vehicles = data.update_vehicles()
    return jsonify(vehicles)

@app.route("/api/routes")
def routes():
    conn = sqlite3.connect('adel-metro.db')
    conn.row_factory = sqlite3.Row
          
    sql = "SELECT * FROM Routes"
    cursor = conn.execute(sql)
    rows = cursor.fetchall()    
    
    conn.close()

    routes = {}

    for row in rows:
        routes[row["RouteID"]] = {
            "colour" : row["Colour"],
            "description" : row["Description"],
            "name" : row["Name"]
        }

    return jsonify(routes)

@app.route("/api/shapes/<trip_id>")
def shapes(trip_id):
    conn = sqlite3.connect('adel-metro.db')
    conn.row_factory = sqlite3.Row

    sql =   "SELECT * FROM Shapes AS S " \
            "JOIN Trips AS T ON S.ShapeID = T.ShapeID " \
            "WHERE TripID = ? " \
            "ORDER BY ShapeSeqNo"
    
    cursor = conn.execute(sql, (trip_id,))
    rows = cursor.fetchall()

    shape = []

    for row in rows:
        position = [row["Latitude"], row["Longitude"]]
        shape.append(position)
    
    return jsonify(shape)

@app.route("/api/stops/<trip_id>")
def stops(trip_id):
    conn = sqlite3.connect('adel-metro.db')
    conn.row_factory = sqlite3.Row

    sql =   "SELECT * FROM StopTimes AS ST " \
            "JOIN Trips AS T ON ST.TripID = T.TripID " \
            "JOIN Stops AS S ON S.StopID = ST.StopID " \
            "WHERE T.TripID = ? " \
                
    cursor = conn.execute(sql, (trip_id,))
    rows = cursor.fetchall()

    stops = []

    for row in rows:
        stop = {
            "name" : row["StopName"],
            "description" : row["StopDescription"],
            "latitude" : row["Latitude"], 
            "longitude" : row["Longitude"],
            "url" : row["Url"],
            "arrivalTime": row["ArrivalTime"],
            "departureTime": row["DepartureTime"]
        }

        stops.append(stop)
    
    return jsonify(stops)

if __name__ == "__main__":
    app.run()
