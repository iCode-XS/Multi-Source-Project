#!/usr/bin/env python3

from core import pipeline
import time
from loguru import logger
import json
import os

# Defaults

total_iter = 0

base_url = 'https://www.pbfa.org'

target_url = 'https://www.pbfa.org/shops'

session = pipeline.init_session(pipeline.chromium_linux)

response = pipeline.fetch_website(session, target_url, timer=20)


def product_link_harvester(response_object, links_list):

    soup = pipeline.parse_website(response_object)

    # container = soup.find('div', class_='animate')

    links_container = soup.find_all('div', class_='content p-2 md:p-4 flex flex-col')

    for x in links_container:

        links = x.find('a')
        links_href = links['href']
        links_list.append(links_href)


def extraction(links_list, storage_list):

    conditional_iter = 0

    while links_list:

        global total_iter

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

        time.sleep(2)

        storage_list.append(capture)

        print(storage_list)

        if conditional_iter == 10:

            with open('website_3.json', 'a') as f:
                json.dump(storage_list, f, indent = 4)

            storage_list.clear()
            conditional_iter = 0

        logger.info('')


if os.path.exists('website_3.json'):
    os.remove('website_3.json')

all_websites = []

data = []

harvest = product_link_harvester(response, all_websites)

extract = extraction(all_websites, data)

logger.info('')

logger.info('')

session.close()
