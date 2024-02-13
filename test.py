from rich import print
from rich.layout import Layout
from rich.console import Group
from rich.panel import Panel
from rich.jupyter import JupyterMixin
from rich.ansi import AnsiDecoder


import plotext as plt

def make_plot(width, height, data):
    plt.clf()


    date = [data["date"]]
    temp = [data["data"]["temp"]]

    plt.bar(date, temp)
    plt.plotsize(width, height)
    plt.theme("dark")
    plt.frame(False)
    return plt.build()

class RichGraph(JupyterMixin):
    def __init__(self, data, maxTemp):
        self.decoder = AnsiDecoder()
        self.data = data
        self.maxTemp = maxTemp

    def __rich_console__(self, console, options):
        self.width = options.max_width or console.width
        self.height = options.height or console.height
        canvas = make_plot(self.width, self.height, self.data)
        self.rich_canvas = Group(*self.decoder.decode(canvas))
        yield self.rich_canvas

def initLayout():
    layout = Layout()

    layout.split_column(
        Layout(name="cityName", size=3),
        Layout(name="date", size=3),
        Layout(name="body"),
        Layout(name="footer", size=3),
    )

    layout["date"].split_row(
        Layout(name="previous"),
        Layout(name="current"),
        Layout(name="next"),
    )  

    return layout 

def makeBarGraph(data, layout):
    layout["body"].split_row(
        Layout(name="day1"),
        Layout(name="day2"),
        Layout(name="day3"),
        Layout(name="day4"),
        Layout(name="day5")
    )

    maxTemp = 0
    for instance in data:
        instance = data[instance]
        if instance["temp"] > maxTemp:
            maxTemp = instance["temp"]

    for i, instance in enumerate(data):
        layoutSlot = layout["body"]["day"+str(i+1)] 
        
        layoutSlot.split_column(
            Layout(name="barGraph"),
            Layout(name="rainPercent", size=3),
            Layout(name="weatherType", size=3),
        )

        # make bar graph with a single bar with plotext
        tempData = {
            "date": instance,
            "data": data[instance],
        }
        graph = RichGraph(tempData, maxTemp)
        layoutSlot["barGraph"].update(Panel(graph))

        # make rainPercentage with Text()
        
        # make weatherType with Text() an emojis        
    
    return layout

def insertInfo(data, layout):
    layout = makeBarGraph(data["data"]["days"], layout)

    return layout

info = {
    "cityName": "Avignon, France",
    "days": {
        "previousDay": "Febr. 27th",
        "currentDay": "Febr. 28th",
        "nextDay": "Febr. 29th",
    },
    "data": {
        "days": {
            "00:00 - 03:00": {
                "temp": 10,
                "rainPercent": 0,
                "windSpeed": 10,
                "windDirection": "N",
                "weatherType": "cloudy", 
            },
            "03:00 - 06:00": {
                "temp": 12,
                "rainPercent": 0,
                "windSpeed": 10,
                "windDirection": "N",
                "weatherType": "cloudy",
            },
            "06:00 - 09:00": {
                "temp": 14,
                "rainPercent": 0,
                "windSpeed": 10,
                "windDirection": "N",
                "weatherType": "cloudy",
            },
            "09:00 - 12:00": {
                "temp": 16,
                "rainPercent": 0,
                "windSpeed": 10,
                "windDirection": "N",
                "weatherType": "cloudy",
            },
            "12:00 - 15:00": {
                "temp": 18,
                "rainPercent": 0,
                "windSpeed": 10,
                "windDirection": "N",
                "weatherType": "cloudy",
            },
        }
    }
}

layout = initLayout()

layout = insertInfo(info, layout)

print(layout)
