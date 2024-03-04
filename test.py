from rich import print
from rich.pretty import Pretty
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

pretty = Pretty(locals())
panel = Panel(Align.center(Text("je suis vieux", style="")))
print(panel)