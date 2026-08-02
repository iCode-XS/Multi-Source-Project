#!/usr/bin/env python3

from core import pipeline
import time
import json
from core import showman
from loguru import logger

target_url = 'https://abac.org/en/members/'

def start(queue5, dqueue5=None, iqueue5=None):

    session = pipeline.init_session(pipeline.chromium_linux)

    response = pipeline.fetch_website(session, target_url, 20)

    parsed = pipeline.parse_website(response)

    container = parsed.find('ul', class_='member-list')

    info = container.find_all('li', class_='member-list-entry')

    data_list = []

    # Defaults

    total_iter = 0

    current_items = 0

    time_per_iter = 0

    for x in info:

        start_time = time.perf_counter()

        total_iter += 1

        total_items = len(container)

        current_items = total_items - total_iter

        capture = {}

        image_container = x.find('div', class_='member-logo-img-container')
        image = image_container.find('img').get('src', 'N/A') if image_container else 'N/A'

        capture['Image Source'] = image

        title_container = x.find('h2', class_='member-name')
        title = title_container.find('a').text

        capture['Bookstore'] = title

        info_container = x.find('div', class_='member-details')
        address = info_container.find('p', class_='member-location address')
        address_safe = address.text if address else 'N/A'
        city = address.find('span', class_='city')
        city_safe = city.text if city else 'N/A'

        capture['Place of Residence'] = city_safe

        contact_source = info_container.find('p', class_='member-email') if info_container else None
        email = contact_source.text.removeprefix('Email: ') if contact_source else 'N/A'

        bba_cont = info_container.find('p', class_='member-website')
        bba = bba_cont.text.removeprefix('Website: ') if bba_cont else 'N/A'

        capture['Books by Author'] = bba
        capture['Contact Source'] = email
        capture['Address'] = address_safe

        data_list.append(capture)

        eta = time_per_iter * current_items
        eta_in_mins = round(eta / 60, 1)
        eta_in_seconds = round(eta % 60, 2)

        percentage = int(total_iter / total_items * 100)

        if percentage == 98:

            percentage = 100

        if queue5: 

            queue5.put(
                f'Current URL: {target_url}\n'
                f'Extracting item: {title}\n'
                f'Estimating time for completion: {eta_in_mins} minute, {eta_in_seconds} seconds\n'
            )
        
        else:

            print(f'Current URL: {target_url}')
            print(f'Extracting item: {title}')
            print(f'Current iterations: {total_iter}')
            print(f'Total items: {total_items}')
            print(f'Percentage: {percentage}')
            print()

        if dqueue5:

            dqueue5.put(capture)

        if iqueue5:

            iqueue5.put(percentage)

        time.sleep(0.1)

        end_time = time.perf_counter()

        time_per_iter = round(end_time - start_time, 2)

    with open('website_5.json', 'w') as f:

        json.dump(data_list, f, indent=4)


def scraper_5(queue5, dqueue5=None, iqueue5=None):

    logger.remove()

    logger.add('website_5.log', rotation='10MB')

    if queue5:

        queue5.put('Initializing Website #5 Ingestion...')

    start(queue5, dqueue5, iqueue5)


if __name__ == '__main__':

    scraper_5(None)
