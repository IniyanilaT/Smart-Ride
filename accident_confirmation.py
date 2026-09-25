def confirm_accident(response):

    response = response.upper()

    if response == "YES":
        return {
            "emergency": False,
            "status": "USER_SAFE",
            "message": "User confirmed they are safe."
        }

    elif response == "NO":
        return {
            "emergency": True,
            "status": "EMERGENCY",
            "message": "User needs emergency assistance."
        }

    elif response == "NO_RESPONSE":
        return {
            "emergency": True,
            "status": "EMERGENCY",
            "message": "No response received. Emergency procedure activated."
        }

    else:
        return {
            "emergency": False,
            "status": "INVALID",
            "message": "Invalid response."
        }
print(confirm_accident("YES"))
print(confirm_accident("NO"))
print(confirm_accident("NO_RESPONSE"))