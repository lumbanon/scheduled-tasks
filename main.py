# To run and test the code you need to update 4 places:
# 1. Change MY_EMAIL/MY_PASSWORD to your own details.
# 2. Go to your email provider and make it allow less secure apps.
# 3. Update the SMTP ADDRESS to match your email provider.
# 4. Update birthdays.csv to contain today's month and day.
# See the solution video in the 100 Days of Python Course for explainations.


# from datetime import datetime
# import pandas
# import random
# import smtplib
# import os

# # import os and use it to get the Github repository secrets
# MY_EMAIL = os.environ.get("MY_EMAIL")
# MY_PASSWORD = os.environ.get("MY_PASSWORD")

# today = datetime.now()
# today_tuple = (today.month, today.day)

# data = pandas.read_csv("birthdays.csv")
# birthdays_dict = {(data_row["month"], data_row["day"])                  : data_row for (index, data_row) in data.iterrows()}
# if today_tuple in birthdays_dict:
#     birthday_person = birthdays_dict[today_tuple]
#     file_path = f"letter_templates/letter_{random.randint(1, 3)}.txt"
#     with open(file_path) as letter_file:
#         contents = letter_file.read()
#         contents = contents.replace("[NAME]", birthday_person["name"])

#     with smtplib.SMTP("YOUR EMAIL PROVIDER SMTP SERVER ADDRESS") as connection:
#         connection.starttls()
#         connection.login(MY_EMAIL, MY_PASSWORD)
#         connection.sendmail(
#             from_addr=MY_EMAIL,
#             to_addrs=birthday_person["email"],
#             msg=f"Subject:Happy Birthday!\n\n{contents}"
#         )
import requests
from twilio.rest import Client
import os

# API & Twilio credentials
api_key = os.environ.get("API_KEY")
account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")

# New environment variables
lat = float(os.environ.get("LATITUDE"))
lon = float(os.environ.get("LONGITUDE"))
virtual_number = os.environ.get("VIRTUAL_NUMBER")
phone_number = os.environ.get("PHONE_NUMBER")

parameters = {
    "lat": lat,
    "lon": lon,
    "appid": api_key,
    "cnt": 4
}

data = requests.get(
    "https://api.openweathermap.org/data/2.5/forecast",
    params=parameters,
)

data.raise_for_status()
weather_data = data.json()

weather_list = []
is_rain = False

for i in range(len(weather_data["list"])):
    weather_list.append(weather_data["list"][i]["weather"][0]["id"])

for weather in weather_list:
    # Weather condition codes: rain is 200–599
    if weather < 700:
        is_rain = True

if is_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="It is going to rain, bring an umbrella ☔",
        from_=virtual_number,
        to=phone_number
    )
    print(message.status)
