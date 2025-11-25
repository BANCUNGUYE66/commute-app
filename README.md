# 🗺️ Commute Comparator

A smart tool to compare travel times and distances between two locations using Driving, Walking, and Cycling modes. Built with Python (Flask) and the OpenRouteService API.

## Features
- **Real-time Routing:** Calculates precise distance and duration.
- **Multi-Mode Comparison:** Compare Driving vs. Walking vs. Cycling side-by-side.
- **Error Handling:** Gracefully handles invalid addresses or ocean routes.

## Installation & Usage (Local)

1. **Clone the repository:**
   \`\`\`bash
   git clone https://github.com/BANCUNGUYE66/commute-app.git
   cd commute-app
   \`\`\`

2. **Install dependencies:**
   \`\`\`bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   \`\`\`

3. **Configure API Key:**
   Create a \`.env\` file in the root directory and add your OpenRouteService key:
   \`\`\`text
   ORS_API_KEY=your_api_key_here
   \`\`\`

4. **Run the application:**
   \`\`\`bash
   python3 app.py
   \`\`\`
   Access at \`http://127.0.0.1:5000\`.

## Technologies Used
- **Backend:** Python, Flask
- **API:** OpenRouteService (Geocoding & Directions)
- **Frontend:** HTML, CSS

## Credits
- Routing data provided by [OpenRouteService](https://openrouteservice.org/).
