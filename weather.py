import requests
from twilio.rest import Client
import os
API_KEY = os.environ.get("API_KEY")
MY_WHATSAPP = os.environ.get("MY_WHATSAPP")
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
END_POINT = os.environ.get("END_POINT")

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"

LAT = 35.657485
LON = 139.694030

parameters = {"lat": LAT, "lon": LON, "appid": API_KEY, "cnt": 6}
response = requests.get(OWM_Endpoint, params=parameters)
response.raise_for_status()

recipients = WHATSAPP_NUM.split()

weather_data = response.json()

is_raining = False
condition_codes = [weather["weather"][0]["id"] for weather in weather_data["list"]]
for condition_code in condition_codes:
    if condition_code < 700:
        is_raining = True
        
if is_raining:

    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    for numero in recipients:
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body="Va a llover hoy, cargate un paraguas o te vas a mojar!!⛈️🌦️☂️☔",
            to=numero
        )
