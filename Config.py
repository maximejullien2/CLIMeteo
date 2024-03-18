import configparser
import re

def setOptions():
    config = configparser.ConfigParser()
    config.read("climeteo.conf")

    # sets the userDefined options
    for option in config["USER_DEFINED"]:
        while True:
            userInput = input(f"Set value for {option} (was {config['USER_DEFINED'][option]}) : ")

            match option:
                case "timezone":
                    try:
                        if userInput != "None":
                            userInput = int(userInput)
                    except ValueError:
                        print("the given input is invalid, it should be an integer or None")
                        continue

                    userInput = str(userInput)
            
                case "numberoftimestamps":
                    try:
                        userInput = int(userInput)
                    except ValueError:
                        print("the given input is invalid, it should be an integer")
                        continue
                
                    userInput = str(userInput)
                
                case "unit":
                    if (userInput != "standard") and (userInput != "metric") and (userInput != "imperial"):
                        print("the give input is invalid, it should be 'standard', 'metric' or 'imperial'")
                        continue

                case "typeofdisplay":
                    if (userInput != "image") and (userInput != "icon"):
                        print("the give input is invalid, it should be 'icon' or 'image'")
                        continue

            config["USER_DEFINED"][option] = userInput
            break

    with open("climeteo.conf", "w") as configFile:
        config.write(configFile)

def resetOptions():
    config = configparser.ConfigParser()
    config.read("climeteo.conf")

    for option in config["DEFAULT"]:
        config["USER_DEFINED"][option] = config["DEFAULT"][option]
    
    with open("climeteo.conf", "w") as configFile:
            config.write(configFile)

def getOption(option):
    config = configparser.ConfigParser()
    config.read("climeteo.conf")

    if option == "timezone":
        if config.get("USER_DEFINED", option) != "None":
            return int(config.get("USER_DEFINED", option)) * 3600

    return config.get("USER_DEFINED", option)

"""
timeZone: translate the time zone (CET, ... or UTC+1) into seconds ( 7200 for UTC+2 ) for the API
numberOfTimeStamps: default at 40, cnt
unit: standard, metric or imperial
typeOfDisplay: image or icon
"""
