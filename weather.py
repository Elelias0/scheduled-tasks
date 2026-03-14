import requests
import os

API_KEY = os.environ.get("API_KEY")
MY_WHATSAPP = os.environ.get("MY_WHATSAPP")
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
END_POINT = os.environ.get("END_POINT")

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"

LAT = 35.657485
LON = 139.694030

parameters = {"lat": LAT, "lon": LON, "appid": API_KEY, "cnt": 2}
response = requests.get(OWM_Endpoint, params=parameters)
response.raise_for_status()

recipients = MY_WHATSAPP.split(",")

weather_data = response.json()

is_raining = False
condition_codes = [weather["weather"][0]["id"] for weather in weather_data["list"]]
for condition_code in condition_codes:
    if condition_code < 700:
        is_raining = True
        
if is_raining:
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    for number in recipients:
        call_api = {
            "messaging_product": "whatsapp",
            "to": f"{number}",
            "type": "template",
            "template": {
                "name": "lluvia",
                "language": {
                    "code": "es_MX"
                },
            }
        }
        response = requests.post(url=END_POINT, json=call_api, headers=headers)
        respo
