#!/usr/bin/env python3

from rich.layout import Layout
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn
from rich.spinner import Spinner

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

layout['bleft'].split_column(
    Layout(name='Extract'),
    Layout(name='Transform'),
    Layout(name='Load')
)

progress = Progress(
    TextColumn('[bold cyan]{task.description}'),
    BarColumn(bar_width=20),
    TaskProgressColumn(),
)

extract = Spinner('dots', text='[bold cyan]Extracting...')
transform = Spinner('dots', text='[bold yellow]Transforming...')
load = Spinner('dots', text='[bold green]Loading...')
