from rich import print
from rich.layout import Layout
from rich.align import Align
from rich.text import Text
from rich.emoji import Emoji
from rich.console import Group
from rich.panel import Panel
from rich.jupyter import JupyterMixin
from rich.ansi import AnsiDecoder
from rich.console import Console
from rich_pixels import Pixels
from PIL import Image
import requests

import callAPI

import datetime

import plotext as plt

def make_plot(width, height, data, maximum,displayMode):
    if displayMode == 1:
        colorsList=[50,44,33,27,18,82,76,124,160,161,196]
        limiteList=[-999,-4,1,6,11,16,21,26,31,36,41]
        temp = [data["temp"]]
    elif displayMode == 2:
        colorsList=[50,44,33,27,18,82,76,124]
        limiteList=[0,20,40,60,80,100,120,140]
        temp = [data["wind_speed"]]
    plt.clf()

    date = [data["date"].strftime("%H:%M")]
    colors = list()
    for temperature in temp : 
        for limite in range(0,len(limiteList)):
            if(limiteList[limite]>temperature):
                break
        colors.append(colorsList[limite])


    # used to make all of the bar graph the same size
    plt.bar([""], [maximum], color="black", width=0)        

    plt.bar(date, temp, color=colors, width=0.2)
    plt.yticks(temp)
    plt.theme("dark")
    plt.frame(False)
    plt.plotsize(width, height)
    return plt.build()

class RichGraph(JupyterMixin):
    def __init__(self, data, maximum,displayMode):
        self.decoder = AnsiDecoder()
        self.data = data
        self.maximum = maximum
        self.displayMode = displayMode

    def __rich_console__(self, console, options):
        self.width = options.max_width or console.width
        self.height = options.height or console.height
        canvas = make_plot(self.width, self.height, self.data, self.maximum,self.displayMode)
        self.rich_canvas = Group(*self.decoder.decode(canvas))
        yield self.rich_canvas

def initLayout(footerSize = 3):
    layout = Layout()

    layout.split_column(
        Layout(name="blank", size=1),
        Layout(name="cityName", size=1),
        Layout(name="date", size=3),
        Layout(name="body"),
        Layout(name="footer", size=footerSize),
    )

    layout["blank"].update(Align(Text(""), align="center", vertical="middle"))

    layout["date"].split_row(
        Layout(name="previous"),
        Layout(name="current"),
        Layout(name="next"),
    )

    layout["body"].split_row(
        Layout(name="day1"),
        Layout(name="day2"),
        Layout(name="day3"),
        Layout(name="day4"),
        Layout(name="day5")
    )

    return layout 

def insertCityName(cityName, layout):
    layout["cityName"].update(Align.center(Text(cityName)))
    return layout

def insertDates(data, indexStart, indexEnd, layout):
    sep = "/"
    daySep = "@"
    dateSep = " - " 

    day = ""
    previousDate = ""
    # if we're at the start of the data, there is no previous date
    if (indexStart > 0):
        day = data[indexStart-1]["hour"]
        previousDate = "< "
        previousDate += day.strftime(f"%d{sep}%m{sep}%Y {daySep} %H:%M")

    layout["date"]["previous"].update(Align(Text(previousDate), align="center", vertical="middle"))
        
    # string formating for the current day
    day = data[indexStart]["hour"]
    currentDate = day.strftime(f"%d{sep}%m{sep}%Y {daySep} %H:%M") 
    currentDate += dateSep

    day = data[indexEnd]["hour"]
    currentDate += day.strftime(f"%d{sep}%m{sep}%Y {daySep} %H:%M")

    layout["date"]["current"].update(Align(Text(currentDate), align="center", vertical="middle"))

    nextDate = ""
    if (indexEnd < len(data)-1):
        day = data[indexEnd+1]["hour"]

        nextDate = day.strftime(f"%d{sep}%m{sep}%Y {daySep} %H:%M")
        nextDate += " >"
    layout["date"]["next"].update(Align(Text(nextDate), align="center", vertical="middle"))

    return layout

def getMaxTemp(data):
    maxTemp = 0
    for instance in data:
        if maxTemp < instance["temperature"]:
            maxTemp = instance["temperature"]

    return maxTemp

def getMaxWindSpeed(data):
    maxWindSpeed = 0
    for instance in data:
        if maxWindSpeed < instance["wind_speed"]:
            maxWindSpeed = instance["wind_speed"]

    return maxWindSpeed

def makeBarGraph(data, start, end, layout,displayMode,iconMode):
    data = data[start:end+1]
    if displayMode == 1:
        maximum = getMaxTemp(data)
    elif displayMode == 2:
        maximum = getMaxWindSpeed(data)
    
    for i, instance in enumerate(data):
        layoutSlot = layout["body"]["day"+str(i+1)] 
        if iconMode == 1:
            layoutSlot.split_column(
                Layout(name="barGraph"),
                Layout(name="additionalInfo", size=1),
                Layout(name="weatherType"),
            )
        elif iconMode == 2:
            layoutSlot.split_column(
                Layout(name="barGraph"),
                Layout(name="additionalInfo", size=1),
                Layout(name="weatherType",size =1),
            )

        # make bar graph with a single bar with plotext
        if displayMode == 1:
            data = {
                "date": instance["hour"],
                "temp": instance["temperature"],
            }
        elif displayMode == 2:
            data = {
                "date": instance["hour"],
                "wind_speed": instance["wind_speed"],
            }
        graph = RichGraph(data, maximum,displayMode)
        layoutSlot["barGraph"].update(Panel(graph))

        # change color depending on the temparature

        # make rainPercentage with Text()
        if displayMode == 1:
            textToShow = f"Precipitation: {instance['precipitation']*100}%"
        elif displayMode ==2:
            textToShow = f"Rafales: {instance['wind_gust']}km/h"
        layoutSlot["additionalInfo"].update(Align(Text(textToShow), align="center", vertical="middle"))
        
        # make weatherType with Text() an emojis
        weatherDict = {
            "01" : "sun_with_face",
            "02" : "sun_behind_large_cloud",
            "03": "cloud",
            "04": "cloud",
            "09": "cloud_with_rain",
            "10": "cloud_with_rain",
            "11": "cloud_with_lightning",
            "13": "snowflake",
            # "13": ":cloud_with_snow:",
            "50": "fog",
        }

        index = instance["weather_icon"][:2]
        icon = weatherDict[index]
        if iconMode == 1:
            icon = Image.open(requests.get(f"https://openweathermap.org/img/wn/{instance['weather_icon']}@2x.png",stream=True).raw).crop((0,25,100,75)).resize((45,20),resample=Image.Resampling.BOX)
            layoutSlot["weatherType"].update(Align(Pixels.from_image(icon), align="center", vertical="middle"))
        elif iconMode == 2:
            layoutSlot["weatherType"].update(Align(Emoji(icon,style=Style(bold=True)), align="center", vertical="middle"))
    
    return layout

def insertFooter(listCommand : dict, layout):
    text = ""
    for i,item in enumerate(listCommand.items()):
        text += item[1] + f" ( {item[0]} ) "
        if (i+1)%2 == 0 and i != 0:
            text += "\n"
        else:
            text += " - "
            
    layout["footer"].update(Align(Text(text), align="center", vertical="middle"))
    return layout

def insertInfo(data, start, end, listCommand, layout,displayMode,iconMode):
    layout = insertCityName(data[0], layout)
    copie = data.copy()
    del copie[0]
    layout = insertDates(copie, start-1, end-1, layout)
    layout = makeBarGraph(copie, start-1, end-1, layout,displayMode,iconMode)
    layout = insertFooter(listCommand, layout)

    return layout

def clear():
    plt.clear_terminal()

def createLayout(info,start,displayMode,iconMode):
    listCommand = {
        "I" : "Cycle through the different icon modes",
        "SpaceBar": "Cycle through the different display modes",
        "V": "Change to wind speed mode",
        "P": "Change to rain percentage mode",
        "R": "Open the search bar to get the information about another city",
        "←": "Show the information about the previous time frame",
        "→": "Show the information about the next time frame",
    }
    layout = initLayout(footerSize=len(listCommand))
    layout = insertInfo(info, start, start+4, listCommand, layout,displayMode,iconMode)
    print(layout)
    