# 🗺️ Commute Comparator

**Commute Comparator** is a smart travel utility designed to help users make informed decisions about their daily transit. By inputting a start and end location, the application queries real-time navigation data to compare travel times and distances across three modes of transport: **Driving**, **Walking**, and **Cycling**.

Unlike basic map apps, this tool provides a side-by-side comparison card view, allowing users to instantly weigh the trade-offs between speed (driving) and health/sustainability (walking/cycling).

---

## 🚀 Features

* **Multi-Mode Comparison:** Simultaneously fetches data for Driving, Walking, and Cycling.
* **Real-Time Data:** Uses the OpenRouteService API for accurate, up-to-date routing.
* **Geocoding:** Automatically converts place names (e.g., "Times Square") into geographic coordinates.
* **Error Handling:** Gracefully handles unreachable locations (e.g., oceans) or invalid addresses.
* **Responsive UI:** Clean, card-based interface built with semantic HTML and CSS.

---

## 🛠️ Technology Stack

* **Backend:** Python 3, Flask
* **Frontend:** HTML5, CSS3
* **API:** OpenRouteService (Geocoding API & Directions V2 API)
* **Version Control:** Git & GitHub

---

## ⚙️ Local Installation & Setup

Follow these steps to run the application on your local machine.

### 1. Prerequisites
* Python 3.6 or higher
* pip (Python package manager)
* An API Key from [OpenRouteService](https://openrouteservice.org/)

### 2. Installation Steps

**Step 1: Clone the repository**
```bash
git clone [https://github.com/BANCUNGUYE66/commute-app.git](https://github.com/BANCUNGUYE66/commute-app.git)
cd commute-app
```

**Step 2: Set up a Virtual Environment**
It is recommended to use a virtual environment to keep dependencies isolated.
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\\Scripts\\activate
```

**Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

**Step 4: Configure Environment Variables**
For security, API keys are not stored in the code. You must create a `.env` file in the root directory.
1. Create a file named `.env`.
2. Add your API key in the following format:
```text
ORS_API_KEY=your_actual_api_key_here
```

**Step 5: Run the Application**
```bash
python3 app.py
```
* By default, the app runs on **Port 5000**.
* Access the app in your browser at: `http://127.0.0.1:5000`

---

## 📡 API Documentation

This project utilizes the **OpenRouteService API**.

1.  **Geocoding Endpoint:**
    * Used to convert user input (city names) into Lat/Long coordinates.
    * Docs: [ORS Geocoding](https://openrouteservice.org/dev/#/api-docs/geocode)
2.  **Directions V2 Endpoint:**
    * Used to calculate the route segments.
    * Profiles used: `driving-car`, `foot-walking`, `cycling-regular`.
    * Docs: [ORS Directions](https://openrouteservice.org/dev/#/api-docs/v2/directions)

---

## 🧠 Challenges & Solutions

During the development of this application, several technical challenges were encountered:

* **Challenge:** The MacOS AirPlay Receiver listens on Port 5000 by default, causing an "Address already in use" error when starting Flask.
    * **Solution:** Investigated the process using port 5000. The application can be configured to run on Port 5001 by modifying `app.run(port=5001)` in `app.py`, or by disabling the AirPlay Receiver in System Settings.

* **Challenge:** Handling routes that are impossible (e.g., walking from New York to London).
    * **Solution:** Implemented a `try-except` block within the routing loop. If the API returns no segments for a specific mode, the application skips that mode without crashing, ensuring a robust user experience.

---

## ☁️ Deployment Architecture (Part 2)

*Note: This section outlines the deployment strategy for the web-01 and web-02 servers.*

The application is designed to be deployed on **Ubuntu 20.04 LTS** servers using **Gunicorn** as the WSGI HTTP Server and **Nginx** as a reverse proxy.

**Load Balancer Configuration:**
HAProxy will be configured on `lb-01` to distribute traffic using a Round Robin algorithm:
1.  **Frontend:** Listens on Port 80.
2.  **Backend:** Forwards requests to `web-01` and `web-02`.
3.  **Health Checks:** Periodically pings the servers to ensure traffic is only sent to healthy instances.

---

## 📜 Credits & Acknowledgments

* **Routing Data:** [OpenRouteService](https://openrouteservice.org/) (based on OpenStreetMap data).
* **Framework:** [Flask](https://flask.palletsprojects.com/).
