import random

def get_manual_sensor_data():
   
    data = {
        "speed": 40,          
        "acceleration": 1.2,  
        "tilt": 5,           
        "vibration": 2        
    }
    return data


def get_random_sensor_data():



    data = {
        "speed": 65,
        "acceleration": 8,
        "tilt": 72,
        "vibration": 18
    }

    return data


def get_simulated_gps():
  
    base_lat = 11.2342   
    base_lng = 78.1023

    data = {
        "latitude": round(base_lat + random.uniform(-0.001, 0.001), 6),
        "longitude": round(base_lng + random.uniform(-0.001, 0.001), 6)
    }
    return data


if __name__ == "__main__":
    print("Manual sensor data:")
    print(get_manual_sensor_data())

    print("\nRandom sensor data:")
    print(get_random_sensor_data())

    print("\nSimulated GPS:")
    print(get_simulated_gps())