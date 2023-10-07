import os
import requests
import smtplib

api_key = os.environ.get("OWM_API_KEY")
city = os.environ.get("CITY")
email = os.environ.get("EMAIL")
email_password = os.environ.get("EMAIL_PASS")


response = requests.get(url=f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}")
response.raise_for_status()
data = response.json()

daily_forecast_codes = []
rain_today = False

for i in range(0, 4):
    daily_forecast_codes.append(data["list"][i]["weather"][0]["id"])

for code in daily_forecast_codes:
    if code < 700:
        rain_today = True

if rain_today:
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user=email, password=email_password)
    connection.sendmail(from_addr=email,
                        to_addrs=email,
                        msg="Subject: Rain alert!\n\nBring an umbrella today!")
    connection.close()
