from flask import Flask, render_template, jsonify
from services import fetch_transport_data, get_shape_data

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.jinja")

@app.route("/api/data")
def api_data():
    data = fetch_transport_data(app.root_path)
    return jsonify(data)

@app.route("/api/shapes/<trip_id>")
def get_shapes(trip_id):
    data = get_shape_data(app.root_path, trip_id)
    return jsonify(data)

if __name__ == "__main__":
    app.run()
