def detect_risk(speed, acceleration, tilt, vibration):
    """
    Classifies the riding situation into:
    NORMAL, RISK, or ACCIDENT.
    """

    
    if (
        acceleration >= 8
        or tilt >= 60
        or vibration >= 9
    ):
        return "ACCIDENT"

    
    if (
        acceleration >= 5
        or tilt >= 30
        or vibration >= 6
        or speed >= 80
    ):
        return "RISK"


    return "NORMAL"


if __name__ == "__main__":

    speed = 40
    acceleration = 10
    tilt = 70
    vibration = 10

    result = detect_risk(
        speed,
        acceleration,
        tilt,
        vibration
    )

    print("Sensor Values")
    print("Speed:", speed)
    print("Acceleration:", acceleration)
    print("Tilt:", tilt)
    print("Vibration:", vibration)

    print("\nRisk Status:", result)