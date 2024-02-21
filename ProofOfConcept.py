from rich import print
from rich.layout import Layout
from rich.align import Align
from rich.text import Text
from rich.emoji import Emoji
from rich.console import Group
from rich.panel import Panel
from rich.jupyter import JupyterMixin
from rich.ansi import AnsiDecoder

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

def initLayout():
    layout = Layout()

    layout.split_column(
        Layout(name="cityName", size=1),
        Layout(name="date", size=3),
        Layout(name="body"),
        Layout(name="footer", size=3),
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

    print(maxTemp)

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
        textToShow = "Precipitation: "
        textToShow += str(instance["precipitation"]*100)
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

def insertFooter(listCommand, layout):
    return

def insertInfo(data, start, end, listCommand, layout):
    layout = insertCityName(data[0], layout)
    del data[0]
    layout = insertDates(data, start, end, layout)
    layout = makeBarGraph(data, start, end, layout)
    layout = insertFooter(listCommand, layout)

    return layout

info = [
    "Morières-lès-Avignon",
    {
        'hour': datetime.datetime(2024, 2, 21, 17, 0), 
        'temperature': 16.43, 
        'feels_like': 15.62, 
        'humidity': 57, 
        'weather_description': 'clear sky', 
        'weather_icon': '01d', 
        'wind_speed': 2.51, 
        'wind_direction': 173, 
        'wind_gust': 3.68, 
        'precipitation': 0
    },
    {
        'hour': datetime.datetime(2024, 2, 21, 20, 0), 
        'temperature': 14.69, 
        'feels_like': 13.86, 
        'humidity': 63, 
        'weather_description': 'scattered clouds', 
        'weather_icon': '03n', 
        'wind_speed': 2.45, 
        'wind_direction': 181, 
        'wind_gust': 3.54, 
        'precipitation': 0
    },
    {
        'hour': datetime.datetime(2024, 2, 21, 23, 0), 
        'temperature': 12.06, 
        'feels_like': 11.28, 
        'humidity': 75, 
        'weather_description': 'broken clouds', 
        'weather_icon': '04n', 
        'wind_speed': 1.99, 
        'wind_direction': 137, 
        'wind_gust': 2.56, 
        'precipitation': 0
    },
    {
        'hour': datetime.datetime(2024, 2, 22, 2, 0), 
        'temperature': 10.08, 
        'feels_like': 9.26, 
        'humidity': 81, 
        'weather_description': 'overcast clouds', 
        'weather_icon': '04n', 
        'wind_speed': 1.76, 
        'wind_direction': 115, 
        'wind_gust': 2.03, 
        'precipitation': 0
    },
    {
        'hour': datetime.datetime(2024, 2, 22, 5, 0), 
        'temperature': 10.22, 
        'feels_like': 9.39, 
        'humidity': 80, 
        'weather_description': 'light rain', 
        'weather_icon': '10n', 
        'wind_speed': 1.15, 
        'wind_direction': 55, 
        'wind_gust': 1.24, 
        'precipitation': 0.42
    },
    {
        'hour': datetime.datetime(2024, 2, 22, 8, 0), 
        'temperature': 9.89, 
        'feels_like': 9.89, 
        'humidity': 81, 
        'weather_description': 'light rain', 
        'weather_icon': '10n', 
        'wind_speed': 0.86, 
        'wind_direction': 128, 
        'wind_gust': 1.35, 
        'precipitation': 0.47
    },
    {
        'hour': datetime.datetime(2024, 2, 22, 11, 0), 
        'temperature': 12.37, 
        'feels_like': 11.46, 
        'humidity': 69, 
        'weather_description': 'overcast clouds', 
        'weather_icon': '04d', 
        'wind_speed': 2.38, 
        'wind_direction': 130, 
        'wind_gust': 4.42, 
        'precipitation': 0.04
    },
]

layout = initLayout()

listCommand = {
    "SpaceBar": "Cycle through the different display modes",
    "V": "Change to wind speed mode",
    "P": "Change to rain percentage mode",
    "LeftArroy": "Show the information about the previous time frame",
    "RightArroy": "Show the information about the next time frame",
    "R": "Open the search bar to get the information about another city",
}

layout = insertInfo(info, 1, 5, listCommand, layout)

print(layout)
