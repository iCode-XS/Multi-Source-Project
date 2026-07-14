#!/usr/bin/env python3

from core import pipeline

base_url = 'https://www.pbfa.org'

target_url = 'https://www.pbfa.org/shops'

session = pipeline.init_session(pipeline.chromium_linux)

response = pipeline.fetch_website(session, target_url, timer=20)

def product_link_harvester(response_object):

    soup = pipeline.parse_website(response_object)

    #container = soup.find('div', class_='animate')

    links_container = soup.find_all('div', class_='content p-2 md:p-4 flex flex-col')

    for x in links_container:

        links = x.find('a')
        links_href = links.get('href', 'N/A') 
        print(links_href)


parse = product_link_harvester(response)
