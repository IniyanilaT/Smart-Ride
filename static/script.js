async function startMonitoring() {

    try {

        const response = await fetch("/analyze");

        const result = await response.json();

        const data = result.sensor_data;

        // Display sensor values
        document.getElementById("speed").innerText = data.speed;
        document.getElementById("acceleration").innerText = data.acceleration;
        document.getElementById("tilt").innerText = data.tilt;
        document.getElementById("vibration").innerText = data.vibration;

        // Display current status
        document.getElementById("rideStatus").innerText =
            result.risk_result;

        // Check for accident
        if (result.risk_result === "ACCIDENT") {

            showAccidentConfirmation();

        } else {

            document.getElementById("alert").innerText =
                "No accident detected.";

        }

    } catch (error) {

        console.error("Monitoring Error:", error);

        document.getElementById("rideStatus").innerText =
            "Connection Error";

        document.getElementById("alert").innerText =
            "Could not connect to backend.";
    }
}
async function loadGPS() {
    console.log("loadGPS function started");

    if (!navigator.geolocation) {

        document.getElementById("gpsStatus").innerText =
            "GPS not supported";

        return;
    }

    document.getElementById("gpsStatus").innerText =
        "Getting real GPS location...";

    navigator.geolocation.getCurrentPosition(

        function(position) {

            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;

            console.log("GPS Location:", latitude, longitude);

            document.getElementById("gpsStatus").innerText =
                "Location: " +
                latitude.toFixed(6) +
                ", " +
                longitude.toFixed(6);

            const map = L.map("map").setView(
                [latitude, longitude],
                15
            );

            L.tileLayer(
                "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
                {
                    attribution: "&copy; OpenStreetMap contributors"
                }
            ).addTo(map);

            L.marker([latitude, longitude])
                .addTo(map)
                .bindPopup("Rider Location")
                .openPopup();

        },

        function(error) {

            console.error("GPS Error:", error);

            document.getElementById("gpsStatus").innerText =
                "GPS unavailable";

        },

        {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0
        }
    );
}

loadGPS();
let responseTimer;
let emergencyTimer;

function showAccidentConfirmation() {

    document.getElementById("confirmation").style.display = "flex";

    document.getElementById("alert").innerText =
        "Accident detected! Please respond.";

    let seconds = 10;

    document.getElementById("responseTimer").innerText =
        "Please respond within " + seconds + " seconds";

    responseTimer = setInterval(function () {

        seconds--;

        document.getElementById("responseTimer").innerText =
            "Please respond within " + seconds + " seconds";

        if (seconds <= 0) {

            clearInterval(responseTimer);

            document.getElementById("responseTimer").innerText =
                "No response received.";

            startEmergencyCountdown();
        }

    }, 1000);
}


function userOK() {

    clearInterval(responseTimer);
    clearInterval(emergencyTimer);

    document.getElementById("confirmation").style.display = "none";

    document.getElementById("alert").innerText =
        "Emergency cancelled. Rider is OK.";

    document.getElementById("rideStatus").innerText =
        "NORMAL";
}


function userNotOK() {

    clearInterval(responseTimer);

    document.getElementById("responseTimer").innerText =
        "Rider selected NO.";

    startEmergencyCountdown();
}


function startEmergencyCountdown() {

    document.getElementById("countdown").style.display = "block";


    let seconds = 10;

    document.getElementById("countdown").innerText =
        "Emergency alert in " + seconds + " seconds";

    emergencyTimer = setInterval(function () {

        seconds--;

        document.getElementById("countdown").innerText =
            "Emergency alert in " + seconds + " seconds";

        if (seconds <= 0) {

            clearInterval(emergencyTimer);

            // Hide accident confirmation popup
            document.getElementById("confirmation").style.display = "none";

            // Show emergency popup
            document.getElementById("emergencyOverlay").style.display = "flex";
            sendEmergencyLocation();

            document.getElementById("emergencyLocation").innerText =
                "Getting rider location...";

            document.getElementById("emergencyStatus").innerText =
                "Sending emergency alert...";

            // Update dashboard status
            document.getElementById("rideStatus").innerText =
                "EMERGENCY";

        }

    }, 1000);
}

async function sendEmergencyLocation() {

    console.log("Emergency location function started");

    if (!navigator.geolocation) {

        document.getElementById("emergencyStatus").innerText =
            "GPS is not supported by this browser.";

        return;
    }

    document.getElementById("emergencyLocation").innerText =
        "Requesting GPS location...";

    document.getElementById("emergencyStatus").innerText =
        "Getting rider location...";

    navigator.geolocation.getCurrentPosition(

        async function(position) {

            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;

            console.log(
                "GPS received:",
                latitude,
                longitude
            );

            document.getElementById("emergencyLocation").innerText =
                "Location: " +
                latitude.toFixed(6) +
                ", " +
                longitude.toFixed(6);

            try {

                const response = await fetch(
                    "/emergency-location",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type": "application/json"
                        },

                        body: JSON.stringify({
                            latitude: latitude,
                            longitude: longitude
                        })
                    }
                );

                console.log(
                    "Backend response status:",
                    response.status
                );

                const result = await response.json();

                console.log(
                    "Backend response:",
                    result
                );

                if (response.ok) {

                    document.getElementById("emergencyStatus").innerText =
                        "📍 Emergency location sent successfully.";

                } else {

                    document.getElementById("emergencyStatus").innerText =
                        "❌ Backend rejected the location.";

                }

            } catch (error) {

                console.error(
                    "Emergency location backend error:",
                    error
                );

                document.getElementById("emergencyStatus").innerText =
                    "❌ Could not send location to backend.";
            }

        },

        function(error) {

            console.error(
                "GPS ERROR:",
                error
            );

            if (error.code === 1) {

                document.getElementById("emergencyStatus").innerText =
                    "❌ GPS permission denied. Allow location access.";

            }

            else if (error.code === 2) {

                document.getElementById("emergencyStatus").innerText =
                    "❌ GPS location unavailable.";

            }

            else if (error.code === 3) {

                document.getElementById("emergencyStatus").innerText =
                    "❌ GPS request timed out.";

            }

            else {

                document.getElementById("emergencyStatus").innerText =
                    "❌ Unable to get GPS location.";
            }

        },

        {
            enableHighAccuracy: true,
            timeout: 20000,
            maximumAge: 0
        }

    );
}