from flask import Flask, render_template, jsonify
from services import fetch_transport_data

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.jinja")

@app.route("/api/data")
def api_data():
    data = fetch_transport_data(app.root_path)
    return jsonify(data)

if __name__ == "__main__":
    app.run()
