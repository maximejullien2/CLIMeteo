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

def make_plot(width, height, data, maxTemp):
    plt.clf()

    date = [data["date"].strftime("%H:%M")]
    temp = [data["temp"]]

    # used to make all of the bar graph the same size
    plt.bar([""], [maxTemp], color="black", width=0)        

    plt.bar(date, temp, color="blue", width=0.2)
    plt.yticks(temp)
    plt.theme("dark")
    plt.frame(False)
    plt.plotsize(width, height)
    return plt.build()

class RichGraph(JupyterMixin):
    def __init__(self, data, maxTemp):
        self.decoder = AnsiDecoder()
        self.data = data
        self.maxTemp = maxTemp

    def __rich_console__(self, console, options):
        self.width = options.max_width or console.width
        self.height = options.height or console.height
        canvas = make_plot(self.width, self.height, self.data, self.maxTemp)
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

def makeBarGraph(data, start, end, layout):
    data = data[start:end+1]
    maxTemp = getMaxTemp(data)

    for i, instance in enumerate(data):
        layoutSlot = layout["body"]["day"+str(i+1)] 
        
        layoutSlot.split_column(
            Layout(name="barGraph"),
            Layout(name="additionalInfo", size=1),
            Layout(name="weatherType"),
        )

        # make bar graph with a single bar with plotext
        tempData = {
            "date": instance["hour"],
            "temp": instance["temperature"],
        }
        graph = RichGraph(tempData, maxTemp)
        layoutSlot["barGraph"].update(Panel(graph))

        # change color depending on the temparature

        # make rainPercentage with Text()
        textToShow = f"Precipitation: {instance['precipitation']*100}%"
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
        layoutSlot["weatherType"].update(Align(Emoji(icon), align="center", vertical="middle"))
        icon = Image.open(requests.get(f"https://openweathermap.org/img/wn/{instance['weather_icon']}@2x.png",stream=True).raw).crop((0,25,100,75)).resize((45,20),resample=Image.Resampling.BOX)
        layoutSlot["weatherType"].update(Align(Pixels.from_image(icon), align="center", vertical="middle"))
    
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

def insertInfo(data, start, end, listCommand, layout):
    layout = insertCityName(data[0], layout)
    del data[0]
    layout = insertDates(data, start, end, layout)
    layout = makeBarGraph(data, start, end, layout)
    layout = insertFooter(listCommand, layout)

    return layout

def createLayout(info):
    listCommand = {
        "SpaceBar": "Cycle through the different display modes",
        "V": "Change to wind speed mode",
        "P": "Change to rain percentage mode",
        "R": "Open the search bar to get the information about another city",
        "←": "Show the information about the previous time frame",
        "→": "Show the information about the next time frame",
    }
    layout = initLayout(footerSize=len(listCommand)//2)
    layout = insertInfo(info, 1, 5, listCommand, layout)
    print(layout)

coords = callAPI.get_coordinates("Morières-lès-Avignon","")
info = callAPI.get_forecast(coords)

createLayout(info)