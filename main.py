#!/usr/bin/env python3

from core import terminal_interface as tui
from loguru import logger
import website_1
import website_2
import website_3
import website_4
import website_5
import multiprocessing
from rich.live import Live
from rich.panel import Panel


def ingestion_1(queue, dqueue, mqueue, squeue, iqueue):

    website_1.scraper_1(queue1, dqueue1, mqueue1, squeue1, iqueue1)


def ingestion_2(queue, dqueue, iqueue):

    website_2.scraper_2(queue2, dqueue2, iqueue2)


def ingestion_3(queue, dqueue, iqueue):

    website_3.scraper_3(queue3, dqueue3, iqueue3)


def ingestion_4(queue, dqueue, iqueue):

    website_4.scraper_4(queue4, dqueue4, iqueue4)


def ingestion_5(queue, dqueue, iqueue):

    website_5.scraper_5(queue5, dqueue5, iqueue5)


if __name__ == '__main__':

    queue1 = multiprocessing.Queue()
    dqueue1 = multiprocessing.Queue()
    mqueue1 = multiprocessing.Queue()
    squeue1 = multiprocessing.Queue()
    iqueue1 = multiprocessing.Queue()

    queue2 = multiprocessing.Queue()
    dqueue2 = multiprocessing.Queue()
    iqueue2 = multiprocessing.Queue()

    queue3 = multiprocessing.Queue()
    dqueue3 = multiprocessing.Queue()
    iqueue3 = multiprocessing.Queue()

    queue4 = multiprocessing.Queue()
    dqueue4 = multiprocessing.Queue()
    iqueue4 = multiprocessing.Queue()

    queue5 = multiprocessing.Queue()
    dqueue5 = multiprocessing.Queue()
    iqueue5 = multiprocessing.Queue()

    p1 = multiprocessing.Process(target=ingestion_1, args=(queue1, dqueue1, mqueue1, squeue1, iqueue1))
    p2 = multiprocessing.Process(target=ingestion_2, args=(queue2, dqueue2, iqueue2))
    p3 = multiprocessing.Process(target=ingestion_3, args=(queue3, dqueue3, iqueue3))
    p4 = multiprocessing.Process(target=ingestion_4, args=(queue4, dqueue4, iqueue4))
    p5 = multiprocessing.Process(target=ingestion_5, args=(queue5, dqueue5, iqueue5))

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()

    with Live(tui.layout, refresh_per_second=10):
        if tui.progress:

            prog1 = tui.progress.add_task('Website #1', total=100, completed=0)
            prog2 = tui.progress.add_task('Website #2', total=100, completed=0)
            prog3 = tui.progress.add_task('Website #3', total=100, completed=0)
            prog4 = tui.progress.add_task('Website #4', total=100, completed=0)
            prog5 = tui.progress.add_task('Website #5', total=100, completed=0)
            tui.layout['bright'].update(Panel(tui.progress, title='Time'))

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

            if not dqueue1.empty():

                dmsg1 = dqueue1.get()
                var = ''

                var1 = dmsg1['Image Source']
                var2 = dmsg1['Bookstore']
                var3 = dmsg1['Place of Residence']
                var4 = dmsg1['Books by Author']
                var5 = dmsg1['Contact Source']

                dic1 = (
                        f'Image Source: {var1}\n'
                        f'Bookstore: {var2}\n'
                        f'Place of Residence: {var3}\n'
                        f'Books by Author: {var4}\n'
                        f'Contact Source: {var5}\n'
                )

                tui.layout['bleft'].update(Panel(tui.table, title='Load data'))

            if not iqueue1.empty():

                mmsg1 = mqueue1.get()
                smsg1 = squeue1.get()
                imsg1 = iqueue1.get()

                tui.progress.update(prog1, total=100, completed=imsg1)

            if not iqueue2.empty():

                imsg2 = iqueue2.get()

                tui.progress.update(prog2, total=100, completed=imsg2)

            if not iqueue3.empty():

                imsg3 = iqueue3.get()
                
                tui.progress.update(prog3, total=100, completed=imsg3)

            if not iqueue4.empty():

                imsg4 = iqueue4.get()

                tui.progress.update(prog4, total=100, completed=imsg4)

            if not iqueue5.empty():

                imsg5 = iqueue5.get()

                tui.progress.update(prog5, total=100, completed=imsg5)
