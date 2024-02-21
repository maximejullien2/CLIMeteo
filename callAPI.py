import requests
from geopy.geocoders import Nominatim
import datetime
import credentials


locator = Nominatim(user_agent="CLIMeteo")
def get_coordinates(city : str):
    """Finds the coordinates of a given city

    Parameters:
      city : The city of which you want to find the coordinates

    Returns:
      map: longitude and latitude of the city
    
    """
    if city == "":
        print("City string is empty")
        return None
    response = locator.geocode(query={"city": city})
    if response == None:
        print("City has not been found")
        return None
    return {
        "latitude": response.latitude,
        "longitude": response.longitude
    }

openweathermap_api_key = credentials.OWM_API_KEY

def get_weather(coordinates : map):
    """Calls the open weather map API to get the current weather

    Parameters:
        coordinates : Coordinates of the city of which you want the weather

    Returns:
        map: Restructured data from the json response containing the relevant informations for the app
    """
    owm_url = f"https://api.openweathermap.org/data/2.5/weather?lat={coordinates['latitude']}&lon={coordinates['longitude']}&appid={openweathermap_api_key}&units=metric"
    owm_response = requests.get(owm_url)
    owm_response_json = owm_response.json()
    return {
        "hour" : datetime.datetime.fromtimestamp(owm_response_json["dt"]) + datetime.timedelta(0,owm_response_json["timezone"]),
        "temperature" : owm_response_json["main"]["temp"],
        "feels_like" : owm_response_json["main"]["feels_like"],
        "humidity" : owm_response_json["main"]["humidity"],
        "weather_description" : owm_response_json["weather"][0]["description"],
        "weather_icon" : owm_response_json["weather"][0]["icon"],
        "wind_speed" : owm_response_json["wind"]["speed"],
        "wind_direction" : owm_response_json["wind"]["deg"],
    }

def get_forecast(coordinates : map):
    """Calls the open weather map API to get the forecast for the next 5 days in increments of 3 hours

    Parameters:
        coordinates : Coordinates of the city of which you want the forecast

    Returns:
        map: First index is the city name, then it is a list of restructured data from the json response containing the relevant informations for the app
    """
    owm_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={coordinates['latitude']}&lon={coordinates['longitude']}&appid={openweathermap_api_key}&units=metric"
    owm_response = requests.get(owm_url)
    owm_response_json = owm_response.json()
    listOfForecasts = []
    listOfForecasts.append(owm_response_json["city"]["name"])
    for timeFrame in owm_response_json["list"]:
        forecast = {
            "hour" : datetime.datetime.fromtimestamp(timeFrame["dt"]) + datetime.timedelta(0,owm_response_json["city"]["timezone"]),
            "temperature" : timeFrame["main"]["temp"],
            "feels_like" : timeFrame["main"]["feels_like"],
            "humidity" : timeFrame["main"]["humidity"],
            "weather_description" : timeFrame["weather"][0]["description"],
            "weather_icon" : timeFrame["weather"][0]["icon"],
            "wind_speed" : timeFrame["wind"]["speed"],
            "wind_direction" : timeFrame["wind"]["deg"],
            "wind_gust" : timeFrame["wind"]["gust"],
            "precipitation" : timeFrame["pop"],
        }
        listOfForecasts.append(forecast)
    return listOfForecasts

#city = "Morieres-les-Avignon"
#city_coordinates = get_coordinates(city)
#city_weather = get_weather(city_coordinates)
#city_forecast = get_forecast(city_coordinates)

#print(city_weather)

#for forecast in city_forecast:
#  print(forecast)