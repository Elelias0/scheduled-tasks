import requests
from bs4 import BeautifulSoup
import smtplib
import os
from email.message import EmailMessage

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
PASSWORD = os.environ.get("PASSWORD")
TO_EMAIL_ADDRESS = os.environ.get("TO_EMAIL_ADDRESS")

SET_PRICE = 250000
url_product = "https://www.amazon.co.jp/Galaxy-Compatible-Smartphone-Lightweight-Waterproof/dp/B0FGNJ77J4/ref=sr_1_2_sspa?crid=1FKV2B7GZP7LS&dib=eyJ2IjoiMSJ9.Odl4CcG5YqbEIoC4vRDSpm0Vdsb32Yfdt64_jXvsr1TAPDa0UO3WRckBCBqRVmU_F9MN_9b0DTLIK08sqqqqNHsforiXge1jED7CPGleQKpw5-5r36gMtObW1m4xshZS5Y2FRdFSxzBmMp8ThwWt_Dc7tzfEG5AKzgTf5CfwMiMJpLAy3PwuurWPTzQAy6D5tyYF-e9Gl-A944804XP-DWpjqy6AXqUEPJUzKxjTaS4dyRGmY_--ripY8nZNxh-ymB67CZQ-iY_UgUOmxizPWqV_ZawNZNDb83qrDzqmWgs.WUMf7CY1Bx0A4LRB1-Tw1uqWX4m7dKaF4cw8xhuyWmk&dib_tag=se&keywords=samsung%2Btri%2Bfold&qid=1773918274&sprefix=samsung%2Bfold%2Btri%2Caps%2C200&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'ja-JP,jp;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Referer': 'https://www.google.com/'
}

response = requests.get(url=url_product, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.content, 'html.parser')

price_list = soup.select(selector="span.a-price-whole")
product_list = soup.select(selector="span#productTitle")

print(price_list)
with open("test.txt","w") as file:
    file.write(f"{soup.prettify()}\n{str(price_list)}\n")
price_int = 500000
try:
    price_string = "".join(price_list[0].string.split(","))
    price_int = int(price_string)
    product_name = product_list[0].string
except:
    price_int = 500000

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
