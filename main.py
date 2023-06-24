import requests
from datetime import datetime
from time import sleep
import math

MY_LAT = 52.056736#51.507351 # Your latitude
MY_LONG = 1.148220#-0.127758 # Yo# ur longitude

MYEMAIL = "******************"
PASSWORD = "*****************"

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

#Your position is within +5 or -5 degrees of the ISS position.


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()
def checkifissoverhead():
    print("in function")
#If the ISS is close to my current position
    if math.isclose(iss_longitude, MY_LONG, abs_tol = 5) and math.isclose(iss_latitude, MY_LAT, abs_tol = 5):
    # and it is currently dark
        if time_now.hour > sunset and time_now.hour < sunrise:
            import smtplib
            with smtplib.SMTP("eu-smtp-outbound-1.mimecast.com", 587) as connection:
                connection.starttls()
                connection.login(user=MYEMAIL, password=PASSWORD)
                connection.sendmail(from_addr="iss_notification@domain.tld",
                                    to_addrs="*******@domain.tld",
                                    msg="subject:iss is over head\n\nThis is an email "
                                        "to tell me the iss is over head")
    else:
        print("iss not close")
        print(math.isclose(iss_longitude, MY_LONG, abs_tol = 5))
        print(math.isclose(iss_latitude, MY_LAT, abs_tol = 5))
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.


i = 1
while i != 0:
    checkifissoverhead()
    sleep(60)



