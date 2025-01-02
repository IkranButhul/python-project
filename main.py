from flask import Flask, request, jsonify
import requests
from twilio.rest import Client

app = Flask(__name__)

# Google API Key and Twilio Credentials
GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"
TWILIO_ACCOUNT_SID = "YOUR_TWILIO_ACCOUNT_SID"
TWILIO_AUTH_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"
TWILIO_PHONE_NUMBER = "YOUR_TWILIO_PHONE_NUMBER"

# Function to get location
def get_location(phone_number):
    # Replace with your actual geolocation service (mocked here)
    geolocation_url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={GOOGLE_API_KEY}"
    response = requests.post(geolocation_url, json={})
    if response.status_code == 200:
        location = response.json()
        return location
    return None

# Twilio SMS Function
def send_sms(phone_number, message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        to=phone_number,
        from_=TWILIO_PHONE_NUMBER,
        body=message
    )

@app.route('/track', methods=['POST'])
def track():
    data = request.json
    phone_number = data.get("phone_number")
    
    # Mock consent message
    send_sms(phone_number, "Consent request: Please reply YES to share your location.")
    
    # Get location (requires user action to consent)
    location = get_location(phone_number)
    if location:
        return jsonify({"status": "success", "location": location}), 200
    return jsonify({"status": "error", "message": "Location not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
