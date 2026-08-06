#!/usr/bin/env python3

from core import pipeline
import time
from loguru import logger
import json
import os
import pandas as pd

# Defaults

total_iter = 0
time_per_iter = 0
total_items = 0

base_url = 'https://www.pbfa.org'

target_url = 'https://www.pbfa.org/shops'


def step_1():

    session = pipeline.init_session(pipeline.chromium_linux)

    response = pipeline.fetch_website(session, target_url, timer=20)

    return session, response

def product_link_harvester(response_object, links_list):

    soup = pipeline.parse_website(response_object)

    # container = soup.find('div', class_='animate')

    links_container = soup.find_all('div', class_='content p-2 md:p-4 flex flex-col')

    for x in links_container:

        links = x.find('a')
        links_href = links['href']
        links_list.append(links_href)
    
    global total_items
    total_items = len(links_list)


def extraction(links_list, storage_list, session, queue3, dqueue3=None, iqueue3=None):

    conditional_iter = 0

    while links_list:

        start_time = time.perf_counter()

        global total_iter

        end_time = 0

        total_iter += 1

        conditional_iter += 1

        capture = {}

        current_url = links_list.pop(0)

        response = pipeline.fetch_website(session, current_url, timer=20)

        soup = pipeline.parse_website(response)

        shop_container = soup.find('div', class_='column profile-title')

        shop = shop_container.find('h1')

        shop_name = shop.text

        address_container = soup.find('div', class_='mb-6 flex flex-row')

        address = soup.find('span', class_='italic text-sand-darker text-sm md:text-base leading-loose').text

        cleaned_address = address.replace(',', ', ')

        bba = soup.find('a', title='Books for Sale by Member')
        bba_link = bba.get('href', 'N/A') if bba else 'N/A'


        member_container = soup.find('div', class_='text-center w-full lg:w-1/5')
        member_link = member_container.find('a', attrs={'href': True})
        member_url = member_link.get('href', 'N/A') if member_link else None

        if member_url:

            response = pipeline.fetch_website(session, member_url, timer=20)

            soup = pipeline.parse_website(response)

            email = soup.find('a', title='Email dealer')
            contact = soup.find('a', title='Call dealer')

            email_info = email.get('href', 'N/A') if email else 'N/A'
            contact_info = contact.get('href', 'N/A') if contact else 'N/A'

            cleaned_email = email_info.removeprefix('mailto:')
            cleaned_contact = contact_info.removeprefix('tel:')

        capture['Image Source'] = 'N/A'
        capture['Bookstore'] = shop_name
        capture['Place of Residence'] = 'N/A'
        capture['Books by Author'] = bba_link
        capture['Contact Source'] = cleaned_email
        capture['Address'] = cleaned_address

        storage_list.append(capture)

        global time_per_iter

        items_left = len(links_list)

        eta = round(time_per_iter * items_left, 2)

        eta_in_minutes = round(eta / 60, 1)

        eta_in_seconds = round(eta % 60, 2)

        percentage = int(total_iter / total_items * 100)

        if queue3:

            queue3.put(
                f'[bold cyan]Current URL[/bold cyan]: {current_url}\n'
                f'[bold yellow]Extracting item[/bold yellow]: {shop_name}\n'
                f'[bold green]Estimating time for completion[/bold green]: {eta_in_minutes} minute, {eta_in_seconds} seconds\n'
            )

        else:

            print(f'Current URL: {current_url}')
            print(f'Extracting item: {shop_name}')
            print(f'Total items: {total_items}')
            print(f'Total iterations: {total_iter}')
            print(f'Percentage: {percentage}')
            print()

        if dqueue3:

            dqueue3.put(capture)

        if iqueue3:

            iqueue3.put(percentage)

        if conditional_iter == 10:

            with open('website_3.json', 'a', encoding='utf-8') as f:
                for a in storage_list:
                    f.write(json.dumps(a) + '\n')

            storage_list.clear()
            conditional_iter = 0

        logger.info('')

        time.sleep(2)

        end_time = time.perf_counter()

        time_per_iter = round(end_time - start_time, 2)


def scraper_3(queue3, dqueue3=None, iqueue3=None, zqueue3=None):

    logger.remove()

    logger.add('website_3.log', rotation='10MB')

    if queue3:

        queue3.put('Initializing Website #3 Ingestion...')

    if os.path.exists('website_3.json'):
        os.remove('website_3.json')

    session, response = step_1()

    all_websites = []

    data = []

    harvest = product_link_harvester(response, all_websites)

    extract = extraction(all_websites, data, session, queue3, dqueue3, iqueue3)

    if queue3:

        queue3.put('Extraction success! Trying to save data into .csv file...')

    zqueue3.put(0)

    if os.path.exists('website_3.json'):

        json_file = pd.read_json('website_3.json', lines=True)
        df = pd.DataFrame(json_file)
        df.to_csv('bookstore_listings.csv', index=False, mode='a', header=False)

    zqueue3.put(20)

    logger.info('')

    logger.info('')

    if queue3:

        queue3.put('Success! Data has been successfully saved to .csv file...')

    session.close()


if __name__ == '__main__':

    scraper_3(None, None)
