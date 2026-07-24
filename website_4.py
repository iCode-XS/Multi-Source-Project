#!/usr/bin/env python3

from core import pipeline
import time


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

def extraction(bs4_object):

    container = bs4_object.find_all('div', class_='_FiCX')

    for x in container:

        title = x.find('span', class_='wixui-rich-text__text', style='font-weight:bold;').text

        contact = x.find('span', class_='wixui-rich-text__text', style='font-size:14px;').text

        address = parsed.find_all('p', class_='font_8 wixui-rich-text__text', style='font-size:14px; line-height:1.6em;')

        total_address = len(address) // 3

        length_addr_list = len(addr_list)

        if length_addr_list <= total_address:
            address_select = address[addr_list.pop(0)]

        print(title)

        print(contact)

        print(address_select.text)

        print()

        time.sleep(6)


a = extraction(parsed)
