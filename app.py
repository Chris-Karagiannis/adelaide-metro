from flask import Flask
from flask import render_template
from services import fetch_transport_data

app = Flask(__name__)

@app.route("/")
def index():
    data = fetch_transport_data(app.root_path)
    return render_template("index.jinja", transport_data=data)

if __name__ == "__main__":
    app.run()
