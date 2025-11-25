#!/usr/bin/env bash
# This script installs and configures a Python Flask application (Geo-Political Data Analyst)
# to run persistently using Gunicorn and Nginx on an Ubuntu 20.04 server.

# Exit immediately if a command exits with a non-zero status
set -e

# --- 1. System Setup & Python Environment ---

echo "--- Updating system packages and installing Python 3.8 ---"
apt-get update -y
# We install python3.8-venv and use python3-pip for compatibility on Ubuntu 20.04
apt-get install -y python3-pip python3.8-venv nginx git build-essential

# Ensure Python 3.8 is the default for venv
if ! command -v python3.8 &> /dev/null
then
    echo "Python 3.8 not found. Installation may fail."
    exit 1
fi

# --- 2. Application Setup ---

REPO_NAME="commute-app"
APP_DIR="/var/www/$REPO_NAME"

echo "--- Cloning repository and setting up application directory ---"

# Clean up any existing deployment
if [ -d "$APP_DIR" ]; then
    rm -rf "$APP_DIR"
fi

# Clone the repository (assumes your user is ubuntu, runs under sudo)
git clone https://github.com/BANCUNGUYE66/$REPO_NAME.git "$APP_DIR"
cd "$APP_DIR"

# Create and activate virtual environment
python3.8 -m venv venv
source venv/bin/activate

# Install dependencies (Flask, Gunicorn, dotenv, requests)
# Note: requirements.txt must be up-to-date in your repository
pip install -r requirements.txt gunicorn

# --- 3. Configuration of Environment Variable (.env) ---

echo "--- Configuring API Key ---"

# Note: This key is valid for Geoapify. The app uses it for compliance.
API_KEY="df009df00d84484ba8888b56e4db7845"
echo "GEOAPIFY_API_KEY=$API_KEY" > .env

# --- 4. Gunicorn System Service Configuration (Web Server) ---

echo "--- Setting up Gunicorn service ---"

# We create a simple shell script to run the app using gunicorn
cat << EOF_GUNICORN > /etc/systemd/system/app_service.service
[Unit]
Description=Gunicorn instance for Flask app
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=$APP_DIR
# Execute Gunicorn: 3 workers, binding to port 5000, running 'app:app' from app.py
ExecStart=$APP_DIR/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF_GUNICORN

# Reload and start the Gunicorn service
systemctl daemon-reload
systemctl start app_service
systemctl enable app_service

# --- 5. Nginx Reverse Proxy Configuration ---

echo "--- Configuring Nginx reverse proxy ---"

# We create the Nginx config file to forward traffic from port 80 to Gunicorn (port 5000)
cat << EOF_NGINX > /etc/nginx/sites-available/app_config
server {
    listen 80;
    server_name _;

    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:5000;
    }
}
EOF_NGINX

# Enable the new configuration and restart Nginx
rm /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/app_config /etc/nginx/sites-enabled/
systemctl restart nginx

echo "Deployment complete. App should be live on port 80."