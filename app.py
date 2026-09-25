import os
from unittest import result
from flask import Flask, request, jsonify, render_template
from sensor_simulator import get_manual_sensor_data, get_random_sensor_data, get_simulated_gps
from risk_detector import detect_risk
from gps_tracker import get_location


app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates"),
    static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
)

system_state = {
    "status": "NORMAL",
    "location": {"latitude": None, "longitude": None}
}
emergency_location = {
    "latitude": None,
    "longitude": None,
    "status": "NO_EMERGENCY"
}
emergency_contact = {
    "name": "Emergency Contact",
    "phone": "+91 8610281675"
}
REQUIRED_KEYS = ["speed", "acceleration", "tilt", "vibration"]


def is_valid_sensor_data(data):
    """
    Checks that incoming sensor data has all required keys
    and that each value is a number (int or float).
    Returns True if valid, False otherwise.
    """
    if not isinstance(data, dict):
        return False
    for key in REQUIRED_KEYS:
        if key not in data:
            return False
        if not isinstance(data[key], (int, float)):
            return False
    return True

@app.route("/emergency-location", methods=["POST"])
def receive_emergency_location():
    
    global emergency_location

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No location data received"
        }), 400

    emergency_location["latitude"] = data.get("latitude")
    emergency_location["longitude"] = data.get("longitude")
    emergency_location["status"] = "EMERGENCY"

    print("Emergency Location Received:")
    print(emergency_location)
    print("Emergency Contact:")
    print(emergency_contact)

    return jsonify({
        "status": "Location received",
        "location": emergency_location
    })
@app.route("/emergency-contact", methods=["GET"])
def get_emergency_contact():

    return jsonify(emergency_contact)


@app.route("/sensor-data", methods=["POST"])
def receive_sensor_data():
    incoming_data = request.get_json()

    if not is_valid_sensor_data(incoming_data):
        return jsonify({
            "error": f"Invalid sensor data. Required keys: {REQUIRED_KEYS}"
        }), 400

    print("Received:", incoming_data)
    return jsonify({
        "status": "received",
        "data": incoming_data
    })


@app.route("/generate-sensor-data", methods=["GET"])
def generate_sensor_data():
    data = get_random_sensor_data()
    print("Generated:", data)
    return jsonify({
        "status": "generated",
        "data": data
    })


@app.route("/system-state", methods=["GET"])
def get_system_state():
    return jsonify(system_state)


@app.route("/system-state", methods=["POST"])
def update_system_state():
    incoming_data = request.get_json()
    new_status = incoming_data.get("status") if incoming_data else None
    valid_statuses = ["NORMAL", "RISK", "ACCIDENT", "EMERGENCY"]

    if new_status not in valid_statuses:
        return jsonify({
            "error": f"Invalid status. Must be one of {valid_statuses}"
        }), 400

    system_state["status"] = new_status
    print("State updated to:", new_status)
    return jsonify({
        "status": "updated",
        "current_state": system_state
    })


@app.route("/analyze", methods=["GET"])
def analyze():
    """
    Full pipeline: generate sensor data + GPS -> analyze -> update state.
    """
    sensor_data = get_random_sensor_data()
    gps_data = get_simulated_gps()

    if not is_valid_sensor_data(sensor_data):
        return jsonify({"error": "Sensor data generation failed"}), 500

    result = detect_risk(
    sensor_data["speed"],
    sensor_data["acceleration"],
    sensor_data["tilt"],
    sensor_data["vibration"]
)

    system_state["status"] = result
    system_state["location"] = gps_data

    print("Analyzed:", sensor_data, "->", result, "at", gps_data)
    return jsonify({
        "sensor_data": sensor_data,
        "gps": gps_data,
        "risk_result": result,
        "current_state": system_state
    })
@app.route("/gps", methods=["GET"])
def gps():

    location = get_location(True)

    return jsonify(location)


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/hospital", methods=["GET"])
def hospital():
    return render_template("hospital.html")   
@app.route("/hospital-location", methods=["GET"])
def hospital_location():

    return jsonify(emergency_location) 
@app.route("/hospital-response", methods=["POST"])
def hospital_response():

    data = request.get_json()

    response = data.get("response") if data else None

    if response not in ["ACCEPTED", "NO_RESPONSE"]:
        return jsonify({
            "error": "Invalid hospital response"
        }), 400

    print("Hospital Response:", response)

    return jsonify({
        "status": "received",
        "hospital_response": response
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)