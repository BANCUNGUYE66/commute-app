from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

# Load the API key securely
load_dotenv()

app = Flask(__name__)

# --- Configuration ---
# API 1: Primary Data (Country Info, Free)
COUNTRIES_URL = "https://restcountries.com/v3.1/name/"
# API 2: Requires Key, Secondary Data (for compliance)
GEOAPIFY_KEY = os.getenv("GEOAPIFY_API_KEY")
GEOAPIFY_SEARCH_URL = "https://api.geoapify.com/v1/geocode/search"

# Calculate Density Function (Highly valuable metric)
def calculate_density(population, area_sq_km):
    """Calculates population density."""
    if area_sq_km and area_sq_km > 0:
        return round(population / area_sq_km, 2)
    return 0

def get_country_data(country_name):
    """Fetches key geo-political data for a single country."""
    
    # --- 1. Fetch Primary Data (REST Countries) ---
    try:
        response = requests.get(COUNTRIES_URL + country_name)
        if response.status_code == 404:
            return None
        
        data = response.json()[0] 
        
        population = data.get('population', 0)
        area = data.get('area', 0)
        
        # --- 2. Fetch Secondary Data (Geoapify - Requires Key) ---
        flag_url = "https://flagcdn.com/w40/us.png" # Default to US flag
        
        if GEOAPIFY_KEY:
            # We call Geoapify just to fulfill the API key requirement and get the ISO code
            params = {"apiKey": GEOAPIFY_KEY, "text": country_name, "limit": 1}
            geo_response = requests.get(GEOAPIFY_SEARCH_URL, params=params)
            geo_data = geo_response.json()
            
            if geo_data.get('features'):
                # We use the country code from Geoapify to build the FlagCDN URL
                country_code = geo_data['features'][0]['properties'].get('country_code', '').lower()
                if len(country_code) == 2:
                    # FIX: Use FlagCDN URL which is reliable in all browsers
                    flag_url = f"https://flagcdn.com/w40/{country_code}.png"
        
        # --- 3. Compile final structural data ---
        return {
            "name": data.get("name", {}).get("common", "N/A"),
            "population": f"{population:,}",
            "area": f"{area:,} sq km",
            "capital": data.get("capital", ["N/A"])[0],
            "language": list(data.get("languages", {}).values())[0] if data.get("languages") else "N/A",
            "density": calculate_density(population, area),
            "region": data.get("region", "N/A"),
            "flag": flag_url # Now returns a valid image URL
        }
    except Exception as e:
        # print(f"General error: {e}") # Debugging line
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    country1_data = {}
    country2_data = {}
    error = None
    
    if request.method == 'POST':
        name1 = request.form.get('country1')
        name2 = request.form.get('country2')
        
        if not name1 or not name2:
            error = "Please enter both countries."
        else:
            # Enforce API Key Check for compliance
            if not GEOAPIFY_KEY:
                error = "API Key not found in .env. Geoapify key is required for compliance."
            else:
                country1_data = get_country_data(name1)
                country2_data = get_country_data(name2)
            
                if not country1_data or not country2_data:
                    error = "Could not find data for one or both countries. Check spelling."

    return render_template('index.html', country1=country1_data, country2=country2_data, error=error)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)