from flask import Flask, request, send_from_directory
import os
import smtplib
import requests
from email.mime.text import MIMEText
from datetime import datetime
import user_agents

app = Flask(__name__)
LOG_FILE = os.path.join(os.path.dirname(__file__), 'honeypot.log')

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "thekingwalk409@gmail.com"  # Replace with your email
EMAIL_PASSWORD = "thekingwalk@1"  # Use App Password if using Gmail
EMAIL_RECEIVER = "thedevilking664@gmail.com"

# Function to get visitor location
def get_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        return f"{data.get('city', 'Unknown')}, {data.get('country', 'Unknown')}"
    except:
        return "Unknown Location"

# Middleware to log visitor details and send email
@app.before_request
def log_request():
    user_agent = user_agents.parse(request.headers.get('User-Agent', ''))
    ip = request.remote_addr
    location = get_location(ip)
    
    log_entry = (
        f"Time: {datetime.now().isoformat()}\n"
        f"IP: {ip}\n"
        f"Location: {location}\n"
        f"Device: {user_agent.device.family}\n"
        f"Browser: {user_agent.browser.family}\n"
        f"-----------------------------------\n"
    )
    
    # Save to log file
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(log_entry)
    
    # Send email
    send_email(log_entry)

# Function to send visitor data via email
def send_email(message):
    try:
        msg = MIMEText(message)
        msg["Subject"] = "🚨 New Visitor Alert - Honeypot Website"
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
    except Exception as e:
        print("Email sending failed:", e)

# Simulate a vulnerable endpoint
@app.route('/admin')
def admin():
    return "Forbidden: You are not authorized to access this page.", 403

# Simulate fake sensitive data
@app.route('/config')
def config():
    return "DB_PASSWORD=supersecretpassword", 200

# Serve the frontend
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.dirname(__file__), filename)

if __name__ == '__main__':
    app.run(port=5500)
