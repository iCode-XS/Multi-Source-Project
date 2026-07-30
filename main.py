#!/usr/bin/env python3

from core import terminal_interface as tui
import website_1
import website_2
import website_3
import website_4
import website_5
import multiprocessing
from rich.live import Live
from rich.panel import Panel


def ingestion_1(queue):

    website_1.scraper_1(queue1)


def ingestion_2(queue):

    website_2.scraper_2(queue2)


def ingestion_3(queue):

    website_3.scraper_3(queue3)


def ingestion_4(queue):

    website_4.scraper_4(queue4)

def ingestion_5(queue):

    website_5.scraper_5(queue5)


if __name__ == '__main__':

    queue1 = multiprocessing.Queue()
    queue2 = multiprocessing.Queue()
    queue3 = multiprocessing.Queue()
    queue4 = multiprocessing.Queue()
    queue5 = multiprocessing.Queue()

    p1 = multiprocessing.Process(target=ingestion_1, args=(queue1,))
    p2 = multiprocessing.Process(target=ingestion_2, args=(queue2,))
    p3 = multiprocessing.Process(target=ingestion_3, args=(queue3,))
    p4 = multiprocessing.Process(target=ingestion_4, args=(queue4,))
    p5 = multiprocessing.Process(target=ingestion_5, args=(queue5,))

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()

    with Live(tui.layout, refresh_per_second=10):

        while p1.is_alive() or p2.is_alive():

            if not queue1.empty():

                msg1 = queue1.get()

                tui.layout['uleft'].update(Panel(msg1, title='Scraper #1'))

            if not queue2.empty():

                msg2 = queue2.get()

                tui.layout['uright'].update(Panel(msg2, title='Scraper #2'))

            if not queue3.empty():

                msg3 = queue3.get()

                tui.layout['lleft'].update(Panel(msg3, title='Scraper #3'))

            if not queue4.empty():

                msg4 = queue4.get()

                tui.layout['lcenter'].update(Panel(msg4, title='Scraper #4'))

            if not queue5.empty():

                msg5 = queue5.get()

                tui.layout['lright'].update(Panel(msg5, title='Scraper #5'))
