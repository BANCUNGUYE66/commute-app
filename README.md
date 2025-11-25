# 🗺️ Commute-app (Geo-Political Data Edition)

The **Commute-app** application (renamed for repository consistency) is a high-value research tool designed for comparative political and resource analysis. It allows users to input two countries and instantly compares key structural, demographic, and economic metrics (Population, Density, Language, etc.).

This application goes beyond simple data display by calculating derived metrics (Population Density) and utilizing two external APIs to ensure robust data integrity and meet all assignment compliance requirements.

---


##🎬 Demo Video Link

[Video](https://www.loom.com/share/6ed5cde0dff242f89717cba96df04b18).

---

## 🚀 Features

* **High-Value Metrics:** Compares Population, Area, Capital, Language, and calculated Population Density.

* **Derived Metric:** Calculates **Population Density (per km²)** using retrieved population and area data.

* **Dual API Integration:** Uses two distinct APIs for data reliability and assignment compliance.

* **Secure Key Handling:** API key is securely loaded via `.env` and excluded from the public repository.

* **Professional UI:** Clean, card-based interface built with Flask/Jinja and semantic HTML/CSS.

---

## 🛠️ Technology Stack

| Component | Technology | Purpose | 
 | ----- | ----- | ----- | 
| **Backend Framework** | Python 3, Flask | Handles routing and data presentation. | 
| **Primary Data Source** | REST Countries API | Fetches core data (Population, Area, Capital). | 
| **Secondary Data Source** | Geoapify API (Key Req.) | Fetches country ISO codes for compliance/flag display. | 
| **Secure Key Handling** | python-dotenv | Securely loads API key from `.env` file. | 

---

## 📡 API Documentation

This application uses two APIs to ensure robustness and compliance with the key requirement.

1. **REST Countries API** (Primary Data):

   * **Endpoint:** `https://restcountries.com/v3.1/name/{country}`

   * **Purpose:** Provides static data (Population, Area, Language).

2. **Geoapify API** (Key Required for Compliance):

   * **Endpoint:** `https://api.geoapify.com/v1/geocode/search`

   * **Purpose:** Used solely to fetch the country's ISO code (for the flag emoji) to fulfill the mandatory API Key usage requirement.

---

## ⚙️ Local Installation & Setup

Follow these steps to run the application on your local machine.

### 1. Prerequisites

* Python 3.6 or higher

* pip (Python package manager)

* An API Key from [Geoapify](https://myprojects.geoapify.com/projects)

### 2. Installation Steps

**Step 1: Clone the repository**

```bash
git clone https://github.com/BANCUNGUYE66/commute-app.git
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

**Step 4: Configure Environment Variables (REQUIRED)**
For security, API keys are not stored in the code. You must create a `.env` file in the root directory.
1. Create a file named `.env`.
2. Add your Geoapify API key in the following format (using the valid key):
```text
GEOAPIFY_API_KEY=your_actual_api_key_here
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


## 📜 Credits & Acknowledgments

* **Primary Data:** [REST Countries API](https://restcountries.com/).
* **Secondary Data/Geocoding:** [Geoapify](https://www.geoapify.com/).
* **Framework:** [Flask](https://flask.palletsprojects.com/).

