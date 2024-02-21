import asyncio
import sys
from os import system

from prompt_toolkit.input import create_input
from prompt_toolkit.keys import Keys

fini = False
#Permet de savoir lorsque si le programme doit etre terminé ou non.

rechercher = False
#Permet de savoir si on doit réaliser une recherche.

mode = 0 
# mode = 0 Correspond au mode pour la précépitation
# mode = 1 Correspond au mode pour le vent

async def main() -> None:
    global fini,rechercher
    done = asyncio.Event()
    input = create_input()

    def keys_ready():
        global fini,rechercher
        for key_press in input.read_keys():
            if key_press.key ==" ":
                #changement de mode
                if(mode == 0):
                    mode =1
                elif(mode == 1):
                    mode =0
                
            elif key_press.key == "v":
                #changement de mode vers le mode vent
                mode = 1
                print("i")
            elif key_press.key == "p":
                #changement de mode vers le mode precipitation
                mode = 0
                print("i")
            elif key_press.key == "right":
                #changement de l'heure vers le futur
                print("i")
            elif key_press.key == "left":
                #changement de l'heure vers le passé
                print("i")
            elif key_press.key == "r":
                #recherche pour une nouvelle ville
                #Mise à zéro du terminal
                rechercher = True
                done.set()
            elif key_press.key == Keys.ControlC:
                fini = True
                done.set()

    with input.raw_mode():
        with input.attach(keys_ready):
            await done.wait()

if len(sys.argv) < 3:
    sys.exit("Le nombre d'argument donné au programme est inssufissant.") 

if sys.argv[1] != "-city":
    sys.exit("Il manque l'argument -city obligatoire pour sélectionner une ville")
 

#city = sys.argv[2]
#city_coordinates = get_coordinates(city)
#city_weather = get_weather(city_coordinates)
#city_forecast = get_forecast(city_coordinates)
#Affichage avec les données

#while fini == False :
asyncio.run(main())
    #if(rechercher):
        #city = input("Recherche par rapport à une ville : ")
        #city_coordinates = get_coordinates(city)
        #city_weather = get_weather(city_coordinates)
        #city_forecast = get_forecast(city_coordinates)
        #system("clear")
        #Affichage avec les données
#    rechercher = False
