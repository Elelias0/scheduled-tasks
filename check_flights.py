import os
from serpapi import GoogleSearch
from twilio.rest import Client

SERPAPI_KEY = os.environ.get("SERPAPI_KEY")
ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
MY_WHATSAPP = os.environ.get("MY_WHATSAPP")
LIMIT = float(130000)
there_is_file = True
there_is_flights = True
error_message = "El archivo de vuelos.txt no se encontro, revisa nuevamente para la proxima ejecucion"
list_my_numbers = MY_WHATSAPP.split(",")

def send_message(mensaje, type_msg):
    if type_msg == 1:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=mensaje,
            to=list_my_numbers[0]
        )
    else:
        for number in list_my_numbers:
            client = Client(ACCOUNT_SID, AUTH_TOKEN)
            message = client.messages.create(
                from_='whatsapp:+14155238886',
                body=mensaje,
                to=number
            )

vuelos = []
try:
    with open("vuelos.txt") as file:
        data = file.readlines()
except FileNotFoundError:
    send_message(error_message, 1)
    there_is_file = False
else:
    for line in data:
        vuelos.append(line.split())
print(vuelos)

#08-01 08-16 -> 180,000

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
        print(search.get_dict())
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

        if there_is_flights:
            if price < LIMIT:
                trip_found_message = f"""
🔔🚨🔔🚨🔔🚨
¡HAY VUELOS BARATOS!
¡¡¡Te dejo la información!!!
El vuelo 🛩️ sale de {from_airport} 
para 3 adultos y 2 niños el precio es de ${price:.2f} MXN 💸💸 🤩
Día de despegue: {dia_de_despegue} 🛫🛫
Día de vuelta: {dia_de_vuelta} 🛬🛬
🚨🔔🚨🔔🚨🔔
⬇️¡¡¡Entra aquí y apresúrate!!!👇\n
{url_to_buy}
"""
                send_message(trip_found_message, 0)
