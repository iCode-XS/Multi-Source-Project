#!/usr/bin/env python3

from rich.layout import Layout
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn

layout = Layout()

layout.split_column(
    Layout(name='upper'),
    Layout(name='lower'),
    Layout(name='lower2')
)

layout['upper'].split_row(
    Layout(name='uleft'),
    Layout(name='uright')
)

layout['lower'].split_row(
    Layout(name='lleft'),
    Layout(name='lcenter'),
    Layout(name='lright')
)

layout['lower2'].split_row(
    Layout(name='bleft', ratio=2),
    Layout(name='bright', ratio=3)
)

table = Table()

table.add_column('Extracting')
table.add_column('Place of Residence')
table.add_column('Books By Author')

progress = Progress(
    TextColumn('[bold cyan]{task.description}'),
    BarColumn(bar_width=20),
    TaskProgressColumn(),
)
