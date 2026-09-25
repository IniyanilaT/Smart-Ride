last_known_location = {
    "latitude": 13.0827,
    "longitude": 80.2707,
    "location": "Chennai"
}


def get_location(gps_available=True):

    if gps_available:

        return {
            "gps_status": "AVAILABLE",
            "latitude": 13.0827,
            "longitude": 80.2707,
            "location": "Chennai"
        }

    else:

        return {
            "gps_status": "UNAVAILABLE",
            "latitude": last_known_location["latitude"],
            "longitude": last_known_location["longitude"],
            "location": last_known_location["location"],
            "message": "Current GPS unavailable. Using last known location."
        }

print("GPS AVAILABLE:")
print(get_location(True))

print("\nGPS UNAVAILABLE:")
print(get_location(False))