#!/usr/bin/env python3

from core import user_agents
from core import pipeline
from core import terminal_interface as tui
import time
import json
from loguru import logger
from rich.panel import Panel

# Default Placeholders

page_number = None
current_item = None
total_page_count = 0
count_per_iter = 0
items_left_per_iter = 0
minute = 0
second = 0
total_pages = 0
current_url = ''
counting = 0
percent_count = 0
one_percent = 0
percentage = 0
final_total_pages = 0

base_url = 'https://www.boekwinkeltjes.nl'

# Target URL

url = 'https://www.boekwinkeltjes.nl/w/list/'

working_url = None

# Fetching the webiste


def first_exec():
    init = pipeline.init_session(user_agents.firefox_linux, http2_enable=False)
    website = pipeline.fetch_website(init, url, 30)

    return init, website


working_url = url
page_number = 1

# Extraction logic begins here

def count_pages(response_var):

    parsed = pipeline.parse_website(response_var)

    next_page_sibling = parsed.find('i', class_='fa fa-arrow-right')
    next_page_link = next_page_sibling.parent['href'] if next_page_sibling else None

    next_page_cont = next_page_sibling.parent if next_page_sibling else None
    total_pages = next_page_cont.find_previous_sibling().text

    final_val = int(total_pages)

    return final_val


def single_page(response_var, list_var, total_page, queue1, dqueue1, mqueue1=None, squeue1=None, iqueue1=None):

    parsed = pipeline.parse_website(response_var)

    table = parsed.find('table')

    tr = table.find_all('tr')

    count_iter = 0

    for num, x in enumerate(tr, start=1):

        start_time = time.perf_counter()

        global one_percent
        global total_pages
        global counting

        counting += 1

        count_iter += 1

        global final_total_pages

        if counting == 1:

            final_total_pages = total_pages * len(tr) - total_pages

            one_percent = int(final_total_pages / 100)

        if num == 1:

            continue

        capture = {}

        image_url_cont = x.find('td')
        author_url = image_url_cont.find('a') if image_url_cont else None
        image_url = author_url.find('img')['src'] if author_url else 'N/A'

        if 'https://images.boekwinkeltjes.nl' in image_url:
            capture['Image Source'] = image_url

        elif 'https://img.boekwinkeltjes.nl' in image_url:
            capture['Image Source'] = image_url

        elif base_url in image_url:
            capture['Image Source'] = image_url

        elif 'N/A' in image_url:
            capture['Image Source'] = image_url

        else:
            capture['Image Source'] = base_url + image_url

        bookstore_cont = image_url_cont.find_next_sibling() if image_url_cont else None
        capture['Bookstore'] = bookstore_cont.text.strip() if bookstore_cont else 'N/A'

        global current_item
        current_item = capture['Bookstore']


        por = bookstore_cont.find_next_sibling() if bookstore_cont else None
        capture['Place of Residence'] = por.text.strip() if por else 'N/A'

        books = por.find_next_sibling() if por else None
        books_a = books.find('a')['href'] if books else None
        capture['Books by Author'] = base_url + books_a if books_a else 'N/A'

        contact_container = books.find_next_sibling() if books else None
        contact_a = contact_container.find('a')['href'] if contact_container else None
        capture['Contact Source'] = base_url + contact_a if contact_a else 'N/A'

        next_page_sibling = parsed.find('i', class_='fa fa-arrow-right')
        next_page_link = next_page_sibling.parent['href'] if next_page_sibling else None

        list_var.append(capture)

        global items_left_per_iter
        global count_per_iter
        global current_url
        global minute
        global second

        total_items = total_pages * len(tr) - total_pages

        items_left_per_iter = total_items - num

        seconds = items_left_per_iter * count_per_iter

        minute = round(seconds / 60, 1)

        second = round(seconds % 60, 2)

        global percent_count


        if counting == one_percent:

            percent_count += 1
            one_percent = counting + counting

        if queue1:
            queue1.put(
                f'[bold cyan]Current URL[/bold cyan]: {working_url}\n'
                f'[bold yellow]Extracting item[/bold yellow]: {current_item}\n'
                f'[bold green]Estimating time for completion[/bold green]: {minute} minute, {second} seconds\n'
            )
        else:
            print(f'Current URL: {working_url}')
            print(f'Extracting item: {current_item}')
            print(f'Percentage Calculation: {one_percent} - {counting}')
            print(f'Percentage: {percent_count}')
            print()

        if dqueue1:
            dqueue1.put(capture)

        if mqueue1:
            mqueue1.put(minute)

        if squeue1:
            squeue1.put(seconds)

        if iqueue1:
            iqueue1.put(percent_count)


        time.sleep(0.2)

        end_time = time.perf_counter()

        time_per_iter = round(end_time - start_time, 2)

        count_per_iter = time_per_iter

    total_pages -= 1

    logger.info('')
    logger.info('')

    next_page = base_url + next_page_link if next_page_link else None

    return next_page


def multi_page(single_page_var, total_page, init, queue1, dqueue1, mqueue1, squeue1, iqueue1):

    global current_url

    current_url = single_page_var

    data = []

    while current_url:

        time.sleep(1)

        next_response = pipeline.fetch_website(init, current_url, 30)

        global page_number
        page_number += 1

        global working_url
        working_url = current_url

        parsed1 = single_page(next_response, data, total_page, queue1, dqueue1, mqueue1, squeue1, iqueue1)

        current_url = parsed1

        with open('website_1.json', 'a') as f:

            json.dump(data, f, indent=4)
            data.clear()


def scraper_1(queue1, dqueue1, mqueue1=None, squeue1=None, iqueue1=None):

    logger.remove()

    logger.add('website_1.log', rotation='10MB')

    if queue1:
        queue1.put('Initializing...')

    global layout

    global total_pages

    init, website = first_exec()

    data = []

    total_pages = count_pages(website)

    time.sleep(1.3)

    page_1 = single_page(website, data, total_pages, queue1, dqueue1, mqueue1, squeue1, iqueue1)

    with open('website_1.json', 'w') as f:

        json.dump(data, f, indent=4)
        data.clear()

    multi_page(page_1, total_pages, init, queue1, dqueue1, mqueue1, squeue1, iqueue1)

    init.close()


if __name__ == '__main__':

    scraper_1(None, None)
