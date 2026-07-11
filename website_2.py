#!/usr/bin/env python3

from core import pipeline
from loguru import logger
import os
import json
import time

logger.add('website_2.log', rotation='10MB')

base_url = 'https://www.antiqbook.com'

target_website = 'https://www.antiqbook.com/dealers'

session = pipeline.init_session(pipeline.chromium_linux)

response = pipeline.fetch_website(session, target_website, timer=20)

# Defaults

time_per_iter = 0
last_page_number = 0
items_per_page = 0
total_iter = 0


def change_page(response_object):

    soup = pipeline.parse_website(response_object)

    next_page = soup.find('a', class_='page-link', rel='next')['href']

    link_logic = base_url + next_page

    return link_logic


def dealer_link_harvester(response_object, list_name):

    soup = pipeline.parse_website(response_object)

    container = soup.find_all('div', style='flex:1;min-width:0;')

    last_page_container = soup.find('nav', class_='mt-4')

    container_child_1 = last_page_container.find('ul')

    li_tags = container_child_1.find_all('li')

    last_page_parent = li_tags[-2]

    last_page = last_page_parent.find('a')['href']

    last_page_holder = last_page.split('=')

    global last_page_number

    last_page_number = int(last_page_holder[-1])

    for item in container:

        dealer_name = item.find('a')['href']
        print('Link:', dealer_name)
        list_name.append(dealer_name)


def extraction(url_list):

    current_iter = 0

    data = []

    global items_per_page

    items_per_page = len(url_list)

    print(items_per_page)

    while url_list:

        global total_iter

        total_iter += 1

        start_time = time.perf_counter()

        capture = {}

        current_iter += 1

        current_url = url_list.pop(0)

        response = pipeline.fetch_website(session, current_url, timer=20)

        soup = pipeline.parse_website(response)

        bookstore_container = soup.find('div', class_='ab-sidebox p-3')

        bookstore = bookstore_container.find('h2').text if bookstore_container else 'N/A'

        cleaned_bookstore = bookstore.strip('\n ')

        capture['Image Source'] = 'N/A'

        capture['Bookstore'] = cleaned_bookstore

        lower_container = soup.find('div', class_='mb-3 small')
        address = lower_container.find('div', class_='flex-grow-1 text-muted').text if lower_container else 'N/A'

        cleaned_address = address.strip()

        final_address_1 = cleaned_address.replace('                    ', ' ')
        final_address_2 = final_address_1.replace('\n', ' ')
        final_address_3 = final_address_2.replace('  ', ',')

        email_container = lower_container.find('div', class_='d-flex mb-2')

        email_child = email_container.find_next_sibling()
        email_child_2 = email_child.find('div', class_='flex-grow-1') if email_child else 'N/A'

        if email_child:
            email = email_child_2.find('a') if email_child_2 else 'N/A'
            email_href = email['href'] if email_child_2 else 'N/A'
        else:
            email = 'N/A'

        contact_container = email_child.find_next_sibling()

        contact = contact_container.find('div', class_='flex-grow-1 text-muted').text if contact_container else 'N/A'
        cleaned_contact = contact.strip('\n ')

        por_container = soup.find('div', class_='ab-meta')
        por_child = por_container.find('span')

        por = por_child.find_next_sibling().text if por_child else 'N/A'

        por_cleaned = por.strip()

        bba_container = soup.find('div', class_='d-flex mb-2')

        bba_child1 = bba_container.find('a')

        bba = bba_child1.find_next_sibling()['href'] if bba_child1 else 'N/A'

        bba_url_logic = base_url + bba if bba_child1 else 'N/A'

        capture['Books by Author'] = bba_url_logic

        capture['Place of Residence'] = por_cleaned

        capture['Contact Source'] = cleaned_contact

        capture['Address'] = final_address_3

        '''if current_iter == 2:
            break'''

        data.append(capture)

        global time_per_iter

        eta = time_per_iter * items_per_page * last_page_number

        eta_in_min = round(eta / 60, 1)

        eta_in_seconds = round(eta % 60, 2)

        print(f'Time taken per iteration: {time_per_iter} seconds')

        print(f'ETA: {eta_in_min} minutes, {eta_in_seconds} seconds')

        print('Total Iterations:', total_iter)

        time.sleep(2)

        end_time = time.perf_counter()

        time_per_iter = round(end_time - start_time, 2)

    with open('website_2.json', 'a') as f:

        json.dump(data, f, indent=4)
        data.clear()


def pagination(session_name, next_url, url_list):

    current_url = next_url

    while current_url:

        response = pipeline.fetch_website(session_name, current_url, timer=20)

        soup = pipeline.parse_website(response)

        link_gen = dealer_link_harvester(response, url_list)

        ingestion = extraction(url_list)

        current_url = change_page(response)


if os.path.exists('website_2.json'):
    os.remove('website_2.json')

dealers_url = []

a = dealer_link_harvester(response, dealers_url)

b = extraction(dealers_url)

c = change_page(response)

d = pagination(session, c, dealers_url)

session.close()
