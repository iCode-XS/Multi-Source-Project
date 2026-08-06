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
import os


current_iter = 0
head = True
save_percent = 0


def ingestion_1(queue, dqueue, mqueue, squeue, iqueue, zqueue):

    website_1.scraper_1(queue1, dqueue1, mqueue1, squeue1, iqueue1, zqueue1)


def ingestion_2(queue, dqueue, iqueue, zqueue):

    website_2.scraper_2(queue2, dqueue2, iqueue2, zqueue2)


def ingestion_3(queue, dqueue, iqueue, zqueue):

    website_3.scraper_3(queue3, dqueue3, iqueue3, zqueue3)


def ingestion_4(queue, dqueue, iqueue, zqueue):

    website_4.scraper_4(queue4, dqueue4, iqueue4, zqueue4)


def ingestion_5(queue, dqueue, iqueue, zqueue):

    website_5.scraper_5(queue5, dqueue5, iqueue5, zqueue5)



if __name__ == '__main__':

    if os.path.exists('bookstore_listings.csv'):

        os.remove('bookstore_listings.csv')

    queue1 = multiprocessing.Queue()
    dqueue1 = multiprocessing.Queue()
    mqueue1 = multiprocessing.Queue()
    squeue1 = multiprocessing.Queue()
    iqueue1 = multiprocessing.Queue()
    zqueue1 = multiprocessing.Queue()

    queue2 = multiprocessing.Queue()
    dqueue2 = multiprocessing.Queue()
    iqueue2 = multiprocessing.Queue()
    zqueue2 = multiprocessing.Queue()

    queue3 = multiprocessing.Queue()
    dqueue3 = multiprocessing.Queue()
    iqueue3 = multiprocessing.Queue()
    zqueue3 = multiprocessing.Queue()

    queue4 = multiprocessing.Queue()
    dqueue4 = multiprocessing.Queue()
    iqueue4 = multiprocessing.Queue()
    zqueue4 = multiprocessing.Queue()

    queue5 = multiprocessing.Queue()
    dqueue5 = multiprocessing.Queue()
    iqueue5 = multiprocessing.Queue()
    zqueue5 = multiprocessing.Queue()


    p1 = multiprocessing.Process(target=ingestion_1, args=(queue1, dqueue1, mqueue1, squeue1, iqueue1, zqueue1))
    p2 = multiprocessing.Process(target=ingestion_2, args=(queue2, dqueue2, iqueue2, zqueue2))
    p3 = multiprocessing.Process(target=ingestion_3, args=(queue3, dqueue3, iqueue3, zqueue3))
    p4 = multiprocessing.Process(target=ingestion_4, args=(queue4, dqueue4, iqueue4, zqueue4))
    p5 = multiprocessing.Process(target=ingestion_5, args=(queue5, dqueue5, iqueue5, zqueue5))

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
            prog6 = tui.progress.add_task('[bold yellow]Writing[/bold yellow][bold green] .csv[/bold green] [bold yellow]file[/bold yellow]', total=100, completed=0)
            tui.layout['bright'].update(Panel(tui.progress, title='Completion', border_style='cyan'))

        tui.layout['Extract'].update(Panel(tui.extract, title='Process', border_style='cyan'))
        tui.layout['Transform'].update(Panel(tui.transform, title='Process', border_style='cyan'))
        tui.layout['Load'].update(Panel(tui.load, title='Process', border_style='cyan'))

        while p1.is_alive() or p2.is_alive() or p3.is_alive() or p4.is_alive() or p5.is_alive():

            if not queue1.empty():

                msg1 = queue1.get()

                tui.layout['uleft'].update(Panel(msg1, title='Website #1', border_style='cyan'))

            if not queue2.empty():

                msg2 = queue2.get()

                tui.layout['uright'].update(Panel(msg2, title='Website #2', border_style='cyan'))

            if not queue3.empty():

                msg3 = queue3.get()

                tui.layout['lleft'].update(Panel(msg3, title='Website #3', border_style='cyan'))

            if not queue4.empty():

                msg4 = queue4.get()

                tui.layout['lcenter'].update(Panel(msg4, title='Website #4', border_style='cyan'))

            if not queue5.empty():

                msg5 = queue5.get()

                tui.layout['lright'].update(Panel(msg5, title='Website #5', border_style='cyan'))

            if not iqueue1.empty():

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

            if not zqueue5.empty():

                zmsg5 = zqueue5.get()

                save_percent += zmsg5

                tui.progress.update(prog6, total=100, completed=save_percent)

            if not zqueue4.empty():

                zmsg4 = zqueue4.get()

                save_percent += zmsg4

                tui.progress.update(prog6, total=100, completed=save_percent)

            if not zqueue3.empty():

                zmsg3 = zqueue3.get()

                save_percent += zmsg3

                tui.progress.update(prog6, total=100, completed=save_percent)

            if not zqueue2.empty():

                zmsg2 = zqueue2.get()

                save_percent += zmsg2

                tui.progress.update(prog6, total=100, completed=save_percent)

            if not zqueue1.empty():

                zmsg1 = zqueue1.get()

                save_percent += zmsg1

                tui.progress.update(prog6, total=100, completed=save_percent)
