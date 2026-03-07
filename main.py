##################### Extra Hard Starting Project ######################
from email.message import EmailMessage
import pandas
import smtplib
import random
import datetime as dt

my_email = "jacob.testing.0139@gmail.com"
password = "vmnw wpvk zuer zwnl"

today = dt.datetime.today()
birthdays_list = pandas.read_csv("birthdays.csv")

# para buscar con mas condiciones dentro de un dataframe
birthdays_today = birthdays_list[
    (birthdays_list["month"] == today.month) &
    (birthdays_list["day"] == today.day)
]

# 4. Send the letter generated in step 3 to that person's email address.
if not birthdays_today.empty:
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user=my_email, password=password)

    with open("letter_templates/subjects.txt", encoding="utf-8") as file:
        l_subjects = file.readlines()

    for index, row in birthdays_today.iterrows():
        letter_num = random.randint(1,8)
        with open(f"letter_templates/letter_{letter_num}.txt", encoding="utf-8") as file:
            body_msg = file.read()

        body_msg = body_msg.replace("[name]", row["name"])

        message = EmailMessage()
        message["Subject"] = random.choice(l_subjects).strip()
        message["From"] = my_email
        message["To"] = row["email"]
        message.set_content(body_msg)
        connection.send_message(message)

    connection.close()



