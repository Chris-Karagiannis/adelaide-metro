from flask import Flask, render_template, jsonify
from services import fetch_transport_data, fetch_shape_data, get_trip_data, check_version_update, get_shape_data, update_data, get_stop_data, get_route_data

app = Flask(__name__)
trip_data = get_trip_data(app.root_path)
shape_data = get_shape_data(app.root_path)
stop_data = get_stop_data(app.root_path)
route_data = get_route_data(app.root_path)

@app.route("/")
def index():

    # Update cached data if there has been a change of version
    if check_version_update(app.root_path):
        global trip_data, shape_data, stop_data, route_data
        update_data(app.root_path)
        trip_data = get_trip_data(app.root_path)
        shape_data = get_shape_data(app.root_path)
        stop_data = get_stop_data(app.root_path)
        route_data = get_route_data(app.root_path)

    return render_template("index.jinja")

@app.route("/api/data")
def api_data():
    data = fetch_transport_data(app.root_path, stop_data, route_data)
    return jsonify(data)

@app.route("/api/shapes/<trip_id>")
def get_shapes(trip_id):
    data = fetch_shape_data(app.root_path, trip_id, trip_data, shape_data)
    return jsonify(data)

if __name__ == "__main__":
    app.run()
