from rich import print
from rich.layout import Layout
from rich.console import Console
from rich.panel import Panel

import plotext as plt

def initLayout():
    layout = Layout()

    layout.split_column(
        Layout(name="cityName"),
        Layout(name="date"),
        Layout(name="body"),
        Layout(name="footer"),
    )

    layout["date"].split_row(
        Layout(name="previous"),
        Layout(name="current"),
        Layout(name="next"),
    )  

    return layout 

"""
data:
[
    [date, temp, rainPercent, weatherType]
    [date, temp, rainPercent, weatherType]
    [date, temp, rainPercent, weatherType]
    [date, temp, rainPercent, weatherType]
    [date, temp, rainPercent, weatherType]
]
"""
def makeBarGraph(data, layout):
    layout["body"].split_row(
        Layout(name="day1"),
        Layout(name="day2"),
        Layout(name="day3"),
        Layout(name="day4"),
        Layout(name="day5")
    )

    for i, instance in enumerate(data):
        layout["body"]["day"+str(i+1)].split_column(
            Layout(name="barGraph"),
            Layout(name="date"),
            Layout(name="rainPercent"),
            Layout(name="weatherType"),
        )

        # make bar graph witha single bar with plotext
        # update through a panel?
        layout["body"]["day"+str(i+1)]["barGraph"].update(Panel("""insert graph here"""))

        # make date with Text()
        # make rainPercentage with Text()
        # make weatherType with Text() an emojis        
    
    return layout

layout = initLayout()

layout = makeBarGraph()

print(layout)
