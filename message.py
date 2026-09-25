import math


hospitals = [
    {
        "name": "City Hospital",
        "latitude": 13.0830,
        "longitude": 80.2710
    },
    {
        "name": "Emergency Care Hospital",
        "latitude": 13.0850,
        "longitude": 80.2750
    },
    {
        "name": "Apollo Hospital",
        "latitude": 13.0674,
        "longitude": 80.2376
    }
]



def calculate_distance(lat1, lon1, lat2, lon2):

    distance = math.sqrt(
        (lat1 - lat2) ** 2 +
        (lon1 - lon2) ** 2
    )

    return distance

def find_nearest_hospital(latitude, longitude):

    nearest_hospital = None
    shortest_distance = float("inf")

    for hospital in hospitals:

        distance = calculate_distance(
            latitude,
            longitude,
            hospital["latitude"],
            hospital["longitude"]
        )

        if distance < shortest_distance:
            shortest_distance = distance
            nearest_hospital = hospital

    return nearest_hospital



location = {
    "latitude": 13.0827,
    "longitude": 80.2707
}

hospital = find_nearest_hospital(
    location["latitude"],
    location["longitude"]
)

print("Accident Location:")
print("Latitude:", location["latitude"])
print("Longitude:", location["longitude"])

print("\nNearest Hospital:")
print(hospital["name"])