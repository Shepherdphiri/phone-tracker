from flask import Flask, request, jsonify, render_template
from datetime import datetime
import os
import json

app = Flask(__name__)

LOCATIONS_FILE = "locations.txt"

@app.route('/')
def dashboard():
    # Load all saved locations
    locations = []
    if os.path.exists(LOCATIONS_FILE):
        with open(LOCATIONS_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(" - ")
                if len(parts) == 2:
                    timestamp, coords = parts
                    lat_lon = coords.replace("Lat: ", "").replace("Lon: ", "").split(", ")
                    if len(lat_lon) == 2:
                        locations.append({
                            "time": timestamp,
                            "lat": float(lat_lon[0]),
                            "lon": float(lat_lon[1])
                        })
    return render_template("dashboard.html", locations=json.dumps(locations))

@app.route('/report', methods=['POST'])
def report_location():
    data = request.get_json()
    lat = data.get('lat')
    lon = data.get('lon')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOCATIONS_FILE, "a") as f:
        f.write(f"{timestamp} - Lat: {lat}, Lon: {lon}\n")

    return jsonify({'status': 'received'})

from flask import send_from_directory

@app.route('/report.html')
def serve_report():
    return send_from_directory('.', 'report.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
