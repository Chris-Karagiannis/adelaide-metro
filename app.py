from flask import Flask, render_template, jsonify
from services import fetch_transport_data, get_shape_data, get_stop_data, check_version_update

app = Flask(__name__)
stops_data = get_stop_data(app.root_path)

@app.route("/")
def index():
    return render_template("index.jinja")

@app.route("/api/data")
def api_data():
    if check_version_update(app.root_path):
        global stops_data
        stops_data = get_stop_data(app.root_path)

    data = fetch_transport_data(app.root_path)
    return jsonify(data)

@app.route("/api/shapes/<trip_id>")
def get_shapes(trip_id):
    stops = []
    
    for id in stops_data["trip_data"][trip_id]:
        stops.append(stops_data["stop_data"][id])

    data = get_shape_data(app.root_path, trip_id, stops)
    return jsonify(data)

if __name__ == "__main__":
    app.run()
