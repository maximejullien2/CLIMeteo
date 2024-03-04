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

import datetime

import plotext as plt

def make_plot(width, height, data, maxTemp):
    colorsList=["lightcyan","paleturquoise","cyan","deepskyblue","dodgerblue","lime","springgreen","tomato","red","indianred","firebrick"]
    limiteList=[-999,-4,1,6,11,16,21,26,31,36,41]
    plt.clf()

    date = [data["date"].strftime("%H:%M")]
    temp = [data["temp"]]
    colors = list()
    for temperature in temp : 
        for limite in range(0,len(limiteList)):
            if(limiteList[limite]>temperature):
                break
        colors.append(colorsList[limite])


    # used to make all of the bar graph the same size
    plt.bar([""], [maxTemp], color="black", width=0)        

    plt.bar(date, temp, color=color, width=0.2)
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
        Layout(name="cityName", size=1),
        Layout(name="date", size=3),
        Layout(name="body"),
        Layout(name="footer", size=footerSize),
    )

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
            Layout(name="additionalInfo", size=3),
            Layout(name="weatherType", size=3),
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
    
    return layout

def insertFooter(listCommand : dict, layout):
    text = ""
    for item in listCommand.items():
        text += item[1] + f" ( {item[0]} )\n"
    layout["footer"].update(Align(Text(text), align="center", vertical="middle"))
    return layout

def insertInfo(data, start, end, listCommand, layout):
    layout = insertCityName(data[0], layout)
    del data[0]
    layout = insertDates(data, start, end, layout)
    layout = makeBarGraph(data, start, end, layout)
    layout = insertFooter(listCommand, layout)

    return layout

def createLayout(info,start):
    listCommand = {
        "SpaceBar": "Cycle through the different display modes",
        "V": "Change to wind speed mode",
        "P": "Change to rain percentage mode",
        "←": "Show the information about the previous time frame",
        "→": "Show the information about the next time frame",
        "R": "Open the search bar to get the information about another city",
    }
    layout = initLayout(footerSize=len(listCommand))
    layout = insertInfo(info, start, start+4, listCommand, layout)
    print(layout)
