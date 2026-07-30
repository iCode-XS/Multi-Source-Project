#!/usr/bin/env python3

from rich.layout import Layout

layout = Layout()

layout.split_column(
    Layout(name='upper'),
    Layout(name='lower')
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
