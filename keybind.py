import asyncio
import sys
from os import system
import callAPI
from prompt_toolkit.input import create_input
from prompt_toolkit.keys import Keys

if sys.argv[1]=="-h":
    messageErreur = "Usage:\n \t python cliMeteo.py -city city [-country country -mode 1] \n\n"
    messageErreur+= "Options and arguments (and corresponding environment variables):\n\n"
    messageErreur+= "-city nomVille  : Pour donner la ville dont on veut récupérer les données météo (Obligatoire ) .\n\n"
    messageErreur+="-country nomPays: Pour donner le pays de la ville dont on veut récupérer les données météo \n                  ( Optionnelle ,valeur origine vide,pour éviter les erreurs \n                  lorsqu'il existe plusieurs villes ayant le même nom ) .\n\n"
    messageErreur+="-mode 1 ou 2    : Pour choisir le mode d’affichage que l’on veut avoir ( Soit 3 heure par 3 heure (mode 1) \n                   ou jour par jour(mode 2 ) (Optionnelle , valeur origine 1).\n\n"
    messageErreur+="-h              : Fourni de l’aide pour l'utilisation du programme (Optionnelle)."
    sys.exit(messageErreur)


fini = False
#To know if the program is finish

rechercher = False
#To know if we need to do a research on a city

mode = 1
# mode = 1 This is the mode for precipitation
# mode = 2 this is the mode to know the speed of wind
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
                if(mode == 1):
                    mode =2
                elif(mode == 2):
                    mode =1
                
            elif key_press.key == "v":
                #Will change mode into speed of wind
                mode = 2
                print("i")
            elif key_press.key == "p":
                #Will change mode into precipitation
                mode = 1
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

if sys.argv[1] == "-country":
    sys.exit("L'argument -country doit ètre donnée après l'argument city") 


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
