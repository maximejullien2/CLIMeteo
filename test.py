import requests
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import datetime

cities = [
    ["Morieres-les-Avignon","France"]
]
df = pd.DataFrame(cities, columns=["city", "country"])

locator = Nominatim(user_agent="CLIMeteo")

def get_coordinates(city, country):
  response = locator.geocode(query={"city": city})
  return {
    "latitude": response.latitude,
    "longitude": response.longitude
  }

df_coordinates = df.apply(lambda x: get_coordinates(x.city, x.country), axis=1)
df = pd.concat([df, pd.json_normalize(df_coordinates)], axis=1)

openweathermap_api_key = "891f73904c111308df04a5472676bfe3"

def get_weather(row):
  owm_url = f"https://api.openweathermap.org/data/2.5/weather?lat={row.latitude}&lon={row.longitude}&appid={openweathermap_api_key}&units=metric"
  owm_response = requests.get(owm_url)
  owm_response_json = owm_response.json()
  sunset_utc = datetime.datetime.fromtimestamp(owm_response_json["sys"]["sunset"])
  return {
      "temp": owm_response_json["main"]["temp"],
      "description": owm_response_json["weather"][0]["description"],
      "icon": owm_response_json["weather"][0]["icon"],
      "sunset_utc": sunset_utc,
      "sunset_local": sunset_utc + datetime.timedelta(seconds=owm_response_json["timezone"])
  }

def get_forecast(row):
  owm_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={row.latitude}&lon={row.longitude}&appid={openweathermap_api_key}"
  owm_response = requests.get(owm_url)
  owm_response_json = owm_response.json()
  print(owm_response_json)
  #sunset_utc = datetime.datetime.fromtimestamp(owm_response_json["sys"]["sunset"])
  #return {
  #    "temp": owm_response_json["main"]["temp"] - 273.15,
  #    "description": owm_response_json["weather"][0]["description"],
  #    "icon": owm_response_json["weather"][0]["icon"],
  #    "sunset_utc": sunset_utc,
  #    "sunset_local": sunset_utc + datetime.timedelta(seconds=owm_response_json["timezone"])
  #}


df_weather = df.apply(lambda x: get_weather(x), axis=1)
df = pd.concat([df, pd.json_normalize(df_weather)], axis=1)

df_forecast = df.apply(lambda x: get_forecast(x),axis=1)

print(df)