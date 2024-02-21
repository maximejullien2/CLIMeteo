import asyncio
import sys
from os import system
import callAPI
from prompt_toolkit.input import create_input
from prompt_toolkit.keys import Keys

fini = False
#To know if the program is finish

rechercher = False
#To know if we need to do a research on a city

mode = 0 
# mode = 0 This is the mode for precipitation
# mode = 1 this is the mode to know the speed of wind
city_forecast = None

async def main() -> None:
    """
    Represent the main programm about keybinds
    """
    global fini,rechercher,city_forecast
    done = asyncio.Event()
    input = create_input()

    def keys_ready():
        """
        For each key who are pressed , we will test if this correspond to a specific type of Keys.
        """
        global fini,rechercher,city_forecast
        for key_press in input.read_keys():
            if key_press.key ==" ":
                #Will change application mode
                if(mode == 0):
                    mode =1
                elif(mode == 1):
                    mode =0
                
            elif key_press.key == "v":
                #Will change mode into speed of wind
                mode = 1
                print("i")
            elif key_press.key == "p":
                #Will change mode into precipitation
                mode = 0
                print("i")
            elif key_press.key == "right":
                #Will change display of time in the futur
                print("i")
            elif key_press.key == "left":
                #Will change display of time in the past
                print("i")
            elif key_press.key == "r":
                #Try to search meteo for a new city
                rechercher = True
                done.set()
            elif key_press.key == Keys.ControlC:
                #Stop the application
                fini = True
                done.set()

    with input.raw_mode():
        with input.attach(keys_ready):
            await done.wait()

if len(sys.argv) < 3:
    sys.exit("Le nombre d'argument donné au programme est inssufissant.") 

if sys.argv[1] != "-city":
    sys.exit("Il manque l'argument -city obligatoire pour sélectionner une ville")



city = sys.argv[2]
city_coordinates = callAPI.get_coordinates(city)
while city_coordinates == None : 
    city = input("Veuillez entrer le nom d'une ville : ")
    city_coordinates = callAPI.get_coordinates(city)
city_weather = callAPI.get_weather(city_coordinates)
city_forecast = callAPI.get_forecast(city_coordinates)

print(city_weather)

for forecast in city_forecast:
  print(forecast)

while fini == False :
    asyncio.run(main())
    if(rechercher):
        city = input("Veuillez entrer le nom d'une ville : ")
        city_coordinates = callAPI.get_coordinates(city)
        while city_coordinates == None : 
            city = input("Veuillez entrer le nom d'une ville : ")
            city_coordinates = callAPI.get_coordinates(city)
        city_weather = callAPI.get_weather(city_coordinates)
        city_forecast = callAPI.get_forecast(city_coordinates)
        system("clear")
        print(city_weather)
        for forecast in city_forecast:
            print(forecast)
    rechercher = False
system("clear")
