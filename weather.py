import requests
from twilio.rest import Client

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"

LAT = 35.657485
LON = 139.694030

parameters = {"lat": LAT, "lon": LON, "appid": api_key, "cnt": 6}
response = requests.get(OWM_Endpoint, params=parameters)
response.raise_for_status()

weather_data = response.json()

is_raining = False
condition_codes = [weather["weather"][0]["id"] for weather in weather_data["list"]]
for condition_code in condition_codes:
    if condition_code < 700:
        is_raining = True
        
if is_raining:

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body="Va a llover hoy, cargate un paraguas o te vas a mojar!!⛈️🌦️☂️☔",
        to=WHATS_APP_NUM
    )
