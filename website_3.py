#!/usr/bin/env python3

from core import pipeline

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


def extraction(links_list):

    while links_list:

        current_url = links_list.pop(0)

        print(current_url)

        response = pipeline.fetch_website(session, current_url, timer=20)

        soup = pipeline.parse_website(response)

        shop_container = soup.find('div', class_='column profile-title')

        shop = shop_container.find('h1')

        shop_name = shop.text

        address_container = soup.find('div', class_='mb-6 flex flex-row')

        address = soup.find('span', class_='italic text-sand-darker text-sm md:text-base leading-loose').text

        break


all_websites = []

harvest = product_link_harvester(response, all_websites)

extract = extraction(all_websites)
