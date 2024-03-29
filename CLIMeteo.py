import asyncio
import sys
from os import system
import callAPI
from prompt_toolkit.input import create_input
from prompt_toolkit.keys import Keys
import GUI

if sys.argv[1]=="-h":
    messageErreur = "Usage:\n \t python cliMeteo.py -city city [-country country -mode 1] \n\n"
    messageErreur+= "Options and arguments (and corresponding environment variables):\n\n"
    messageErreur+="-city nomVille  : Pour donner la ville dont on veut récupérer les données météo (Obligatoire ) .\n\n"
    messageErreur+="-country nomPays: Pour donner le pays de la ville dont on veut récupérer les données météo \n                  ( Optionnelle ,valeur origine vide,pour éviter les erreurs) \n                  lorsqu'il existe plusieurs villes ayant le même nom ) .\n\n"
    messageErreur+="-h              : Fourni de l’aide pour l'utilisation du programme (Optionnelle)."
    sys.exit(messageErreur)


fini = False
#To know if the program is finished

rechercher = False
#To know if we need to do a research on a city

displayMode = 1
# mode = 1 This is the mode for precipitation
# mode = 2 this is the mode to know the speed of wind
city_forecast = None

#When we will star to display day in API
start=1

#iconMode = 1 This will use pixels to display icon
#iconMode = 2 This will use emoji to display icon
iconMode=1

async def main() -> None:
    """
    Represent the main programm about keybinds
    """
    global fini,rechercher,city_forecast,start,displayMode,iconMode
    done = asyncio.Event()
    input = create_input()

    def keys_ready():
        """
        For each key who are pressed , we will test if this correspond to a specific type of Keys.
        """
        global fini,rechercher,city_forecast,start,displayMode,iconMode
        for key_press in input.read_keys():
            if key_press.key ==" ":
                #Will change application display mode
                if(displayMode == 1):
                    displayMode = 2
                elif(displayMode == 2):
                    displayMode = 1
                GUI.clear()
                GUI.createLayout(city_forecast,start,displayMode,iconMode)
            elif key_press.key == "v":
                #Will change display mode into speed of wind
                displayMode = 2
                GUI.clear()
                GUI.createLayout(city_forecast,start,displayMode,iconMode)
            elif key_press.key == "p":
                #Will change display mode into precipitation
                displayMode = 1
                GUI.clear()
                GUI.createLayout(city_forecast,start,displayMode,iconMode)
            elif key_press.key == "i":
                #Will change icon mode
                if iconMode == 1 :
                    iconMode = 2
                elif iconMode == 2:
                    iconMode = 1
                GUI.clear()
                GUI.createLayout(city_forecast,start,displayMode,iconMode)
            elif key_press.key == "right":
                #Will change display of time in the futur
                start+=5
                if(start>40):
                    start=36
                GUI.clear()
                GUI.createLayout(city_forecast,start,displayMode,iconMode)
            elif key_press.key == "left":
                #Will change display of time in the past
                start-=5
                if(start<1):
                    start=1
                GUI.clear()
                GUI.createLayout(city_forecast,start,displayMode,iconMode)
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

system("clear")

city = sys.argv[2]
country = None
if len(sys.argv)==5 :
    if sys.argv[3] != "-country":
        sys.exit("L'argument -country n'existe pas ou est mal placé")
    country = sys.argv[4]
city_coordinates = callAPI.get_coordinates(city,country)
while city_coordinates == None : 
    city = input("Veuillez entrer le nom d'une ville : ")
    country = input("Veuillez entrer le pays de ville que vous avez écrit (Non obligatoire): ")
    if country == "":
        country = None
    city_coordinates = callAPI.get_coordinates(city,country)
city_weather = callAPI.get_weather(city_coordinates)
city_forecast = callAPI.get_forecast(city_coordinates)

while fini == False :
    GUI.createLayout(city_forecast,start,displayMode,iconMode)
    asyncio.run(main())
    if(rechercher):
        city = input("Veuillez entrer le nom d'une ville : ")
        country = input("Veuillez entrer le pays de ville que vous avez écrit (Non obligatoire): ")
        if country == "":
            country = None
        city_coordinates = callAPI.get_coordinates(city,country)
        while city_coordinates == None : 
            city = input("Veuillez entrer le nom d'une ville : ")
            country = input("Veuillez entrer le pays de ville que vous avez écrit (Non obligatoire): ")
            if country == "":
                country = None
            city_coordinates = callAPI.get_coordinates(city,country)
        city_weather = callAPI.get_weather(city_coordinates)
        city_forecast = callAPI.get_forecast(city_coordinates)
        system("clear")
        GUI.clear()
        start=1
    rechercher = False
system("clear")
GUI.clear()
