from termcharts import bar
from rich import print
from rich.layout import Layout
from rich.console import Console
from rich.panel import Panel

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

charts = [
    bar({'8:00': 18}, title="", mode="v", rich=True),
    bar({'9:00': 19}, title="", mode="v", rich=True),
    bar({'10:00': 15}, title="", mode="v", rich=True),
    bar({'11:00': 17}, title="", mode="v", rich=True),
    bar({'12:00': 18}, title="", mode="v", rich=True),
    bar({'13:00': 20}, title="", mode="v", rich=True),
]

chartRenderable = [Panel(i, expand = True) for i in charts]
layout["body"].update(chartRenderable)


print(layout)