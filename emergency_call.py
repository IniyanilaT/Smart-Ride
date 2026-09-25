import json
from datetime import datetime


def save_emergency_data(accident, location):

    data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "accident": accident,
        "location": location,
        "network": "UNAVAILABLE",
        "status": "STORED_LOCALLY"
    }

    with open("emergency_data.json", "w") as file:
        json.dump(data, file, indent=4)

    return data