#!/usr/bin/env python3

from core import pipeline
import time
import json


# Defaults

time_per_iter = 0
current_iter = 0

# Code 

base_url = 'https://www.ioba.org/'

target_url = 'https://www.ioba.org/members-directory'

session = pipeline.init_session(pipeline.chromium_linux)

response = pipeline.fetch_website(session, target_url, timer=20)

parsed = pipeline.parse_website(response)

# Number pattern generator for messy address logic
# Don't blame me, this is my current skill level! Logic might be different if I was practicing css selectors based scraping

addr_list = [2]

addr_num = 2

for x in range(9):

    addr_num += 3

    addr_list.append(addr_num)

# Extraction function

def extraction(bs4_object, list_name):

    container = bs4_object.find_all('div', class_='_FiCX')

    for x in container:

        capture = {}

        global current_iter

        global time_per_iter

        current_iter += 1

        start_time = time.perf_counter()

        title = x.find('span', class_='wixui-rich-text__text', style='font-weight:bold;').text

        contact = x.find('span', class_='wixui-rich-text__text', style='font-size:14px;').text

        address = parsed.find_all('p', class_='font_8 wixui-rich-text__text', style='font-size:14px; line-height:1.6em;')

        total_address = len(address) // 3

        length_addr_list = len(addr_list)

        if length_addr_list <= total_address:
            address_select = address[addr_list.pop(0)]

        print(f'Current URL: {target_url}')

        print(f'Extracting item: {title}')

        total_items = len(container)

        items_left = total_items - current_iter

        eta = time_per_iter * items_left

        eta_in_mins = round(eta / 60, 1)

        eta_in_seconds = round(eta % 60, 2)

        print(f'Estimated Time of Completion: {eta_in_mins} minutes, {eta_in_seconds} seconds')

        print()

        capture['Image Source'] = 'N/A'

        capture['Bookstore'] = title

        capture['Place of Residence'] = 'N/A'

        capture['Books by Author'] = 'N/A'

        capture['Contact Source'] = contact

        capture['Address'] = address_select.text

        list_name.append(capture)

        time.sleep(8)

        end_time = time.perf_counter()

        time_per_iter = round(end_time - start_time, 2)

    with open('website_4.json', 'w') as f:

        json.dump(list_name, f, indent=4)


data = []

a = extraction(parsed, data)
