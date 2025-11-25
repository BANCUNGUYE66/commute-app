from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
API_KEY = os.getenv("ORS_API_KEY")

MODES = {'Driving': 'driving-car', 'Walking': 'foot-walking', 'Cycling': 'cycling-regular'}

def get_coordinates(place_name):
    url = "https://api.openrouteservice.org/geocode/search"
    params = {"api_key": API_KEY, "text": place_name, "size": 1}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if data['features']:
            return data['features'][0]['geometry']['coordinates']
    except Exception:
        pass
    return None

def format_duration(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    return f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"

@app.route('/', methods=['GET', 'POST'])
def index():
    routes = []
    error = None
    origin = ""
    dest = ""
    
    if request.method == 'POST':
        origin = request.form.get('origin')
        dest = request.form.get('destination')
        start_coords = get_coordinates(origin)
        end_coords = get_coordinates(dest)
        
        if not start_coords or not end_coords:
            error = "Could not find one of those locations."
        else:
            for mode, profile in MODES.items():
                url = f"https://api.openrouteservice.org/v2/directions/{profile}"
                params = {"api_key": API_KEY, "start": f"{start_coords[0]},{start_coords[1]}", "end": f"{end_coords[0]},{end_coords[1]}"}
                try:
                    data = requests.get(url, params=params).json()
                    if 'features' in data:
                        summary = data['features'][0]['properties']['segments'][0]
                        routes.append({
                            "mode": mode,
                            "distance": f"{round(summary['distance'] / 1000, 2)} km",
                            "duration": format_duration(summary['duration'])
                        })
                except Exception:
                    pass
            if not routes: error = "No routes found."

    return render_template('index.html', routes=routes, error=error, origin=origin, dest=dest)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
