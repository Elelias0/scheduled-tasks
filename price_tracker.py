import requests
from bs4 import BeautifulSoup
import smtplib
import os
from email.message import EmailMessage

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
PASSWORD = os.environ.get("PASSWORD")
TO_EMAIL_ADDRESS = os.environ.get("TO_EMAIL_ADDRESS")

SET_PRICE = 250000
url_product = "https://amzn.asia/d/0auRuZOl"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

response = requests.get(url=url_product, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.content, 'html.parser')

price_list = soup.select(selector="span.a-price-whole")
product_list = soup.select(selector="span#productTitle")

print(price_list)
with open("test.txt","w") as file:
    file.write(f"{soup.prettify()}\n{str(price_list)}\n")

price_string = "".join(price_list[0].string.split(","))
price_int = int(price_string)
product_name = product_list[0].string

if price_int <= SET_PRICE:
    connection = smtplib.SMTP('smtp.gmail.com', 587)
    connection.starttls()
    connection.login(EMAIL_ADDRESS, PASSWORD)

    body_msg = f"""
Your desired product:\n{product_name}\ncost now ￥{price_int}\nGo!!! 
"""

    message = EmailMessage()
    message["Subject"] = f"Your product is now cheaper at Amazon JP!!"
    message["From"] = EMAIL_ADDRESS
    message["To"] = TO_EMAIL_ADDRESS
    message.set_content(body_msg)
    connection.send_message(message)
    connection.close()
