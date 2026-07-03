#!/usr/bin/env python3

from core import pipeline
from core import showman
import time
import json
from loguru import logger

# Initiating a session

logger.remove()

logger.add('website_1.log', rotation='10MB')

# Default Placeholders

page_number = None
current_item = None
total_page_count = 0
count_per_iter = 0
items_left_per_iter = 0

init = pipeline.init_session(pipeline.chromium_linux, http2_enable=True)
base_url = 'https://www.boekwinkeltjes.nl'

# Target URL

url = 'https://www.boekwinkeltjes.nl/w/list/'

working_url = None

# Fetching the webiste

website = pipeline.fetch_website(init, url, 30)

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


def single_page(response_var, list_var, total_page):

    parsed = pipeline.parse_website(response_var)

    table = parsed.find('table')

    tr = table.find_all('tr')

    print(f'Current URL: {working_url}')

    count_iter = 0

    for num, x in enumerate(tr, start=1):

        start_time = time.perf_counter()

        count_iter += 1

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

        print(f'Extrating item: {current_item}')

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

        global total_pages
        global items_left_per_iter
        global count_per_iter

        items_left_per_iter = (total_pages * len(tr) - total_pages) - num

        seconds = items_left_per_iter * count_per_iter

        minute = seconds / 60

        second = seconds % 60

        print('Estimated Time of Completion:', round(minute, 1), 'minutes,', round(second, 2), 'seconds left')

        time.sleep(0.2)

        end_time = time.perf_counter()

        time_per_iter = round(end_time - start_time, 2)

        count_per_iter = time_per_iter

        showman.mv_clr()
        showman.mv_clr()

    showman.mv_clr()

    total_pages -= 1

    logger.info('')
    logger.info('')

    next_page = base_url + next_page_link if next_page_link else None

    return next_page


def multi_page(single_page_var, total_page):

    current_url = ''

    current_url = single_page_var

    data = []

    while current_url:

        time.sleep(1)

        next_response = pipeline.fetch_website(init, current_url, 30)

        global page_number
        page_number += 1

        global working_url
        working_url = current_url

        parsed1 = single_page(next_response, data, total_page)

        current_url = parsed1

        with open('website_1.json', 'a') as f:

            json.dump(data, f, indent=4)
            data.clear()


data = []

print('Multi Source Project | Version 1.4 Main')

print()

total_pages = count_pages(website)

showman.carriage_dotprint('Initiating', wipe_space=True)

time.sleep(1.3)

showman.carriage_dotprint('Ingestion in progress | Please wait', next_line=True)

print()

page_1 = single_page(website, data, total_pages)

with open('website_1.json', 'w') as f:

    json.dump(data, f, indent=4)
    data.clear()

multi_page(page_1, total_pages)

showman.mv_clr()
showman.mv_clr()

init.close()
