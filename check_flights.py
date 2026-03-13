import os
from serpapi import GoogleSearch
import requests

SERPAPI_KEY = os.environ.get("SERPAPI_KEY")
MY_WHATSAPP = os.environ.get("MY_WHATSAPP")
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
END_POINT = os.environ.get("END_POINT")

LIMIT = float(130000)
there_is_file = True
there_is_flights = True
list_my_numbers = MY_WHATSAPP.split(",")

vuelos = []
try:
    with open("vuelos.txt") as file:
        data = file.readlines()
except FileNotFoundError:
    there_is_file = False
else:
    for line in data:
        vuelos.append(line.split())

if there_is_file:
    for vuelo in vuelos:
        dia_de_despegue = vuelo[0]
        dia_de_vuelta = vuelo[1]
        params = {
            "engine": "google_flights",
            "departure_id": "MEX,NLU",
            "arrival_id": "NRT",
            "currency": "MXN",
            "outbound_date": dia_de_despegue,
            "return_date": dia_de_vuelta,
            "api_key": SERPAPI_KEY,
            "adults": "3",
            "children": "2",
            "sort_by": "2",
            "stops": "2",
            "include_airlines": "AM,NH"
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        price = 0
        from_airport = ""
        try:
            data_cheaper_flight = results["other_flights"][0]
        except IndexError:
            there_is_flights = False
        else:
            price = float(data_cheaper_flight["price"])
            from_airport = data_cheaper_flight["flights"][0]["departure_airport"]["name"]
        finally:
            url_to_buy = results["search_metadata"]["google_flights_url"]
            url_to_buy = url_to_buy.replace("https://google.com/", "")

        if there_is_flights:
            if price < LIMIT:
                headers = {
                    "Authorization": f"Bearer {WHATSAPP_TOKEN}",
                    "Content-Type": "application/json"
                }
                for number in list_my_numbers:
                    call_api = {
                        "messaging_product": "whatsapp",
                        "to": f"{number}",
                        "type": "template",
                        "template": {
                            "name": "flights_2", #flights_2
                            "language": {
                                "code": "en"
                            },
                            "components": [{
                                "type": "body",
                                "parameters": [{
                                    "type": "text",
                                    "parameter_name": "airport", # airport
                                    "text": f"{from_airport}" 
                                },
                                {
                                    "type": "text",
                                    "parameter_name": "test", #test
                                    "text": f"{price:.2f}" 
                                },
                                {
                                    "type": "text",
                                    "parameter_name": "dia_de_despegue",
                                    "text": f"{dia_de_despegue}"
                                },
                                {
                                    "type": "text",
                                    "parameter_name": "dia_de_vuelta",
                                    "text": f"{dia_de_vuelta}"
                                }]
                            },
                            {
                                "type": "button",  # Cambiado de 'buttons' a 'button'
                                "sub_type": "url",  # Obligatorio para botones de enlace
                                "index": "0",  # El primer botón de tu plantilla
                                "parameters": [{
                                        "type": "text",
                                        "text": f"{url_to_buy}"  # Solo la parte dinámica que completa la URL
                                }]
                            }]
                        }
                    }
                    response = requests.post(url=END_POINT, json=call_api, headers=headers)
