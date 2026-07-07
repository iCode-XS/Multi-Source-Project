#!/usr/bin/env python3

from core import pipeline
from loguru import logger

logger.add('website_2.log', rotation='10MB')

base_url = 'https://www.antiqbook.com'

target_website = 'https://www.antiqbook.com/dealers'

session = pipeline.init_session(pipeline.chromium_linux)

response = pipeline.fetch_website(session, target_website, timer=20)


def change_page(response_object):

    soup = pipeline.parse_website(response_object)

    next_page = soup.find('a', class_='page-link', rel='next')['href']

    link_logic = base_url + next_page

    return link_logic


def dealer_link_harvester(response_object, list_name):

    soup = pipeline.parse_website(response_object)

    container = soup.find_all('div', style='flex:1;min-width:0;')

    for item in container:

        dealer_name = item.find('a')['href']
        print('Link:', dealer_name)
        list_name.append(dealer_name)


def extraction(list_name):

    current_iter = 0

    while list_name:

        current_iter += 1
        
        current_url = list_name.pop(0)

        response = pipeline.fetch_website(session, current_url, timer=20)

        soup = pipeline.parse_website(response)

        bookstore_container = soup.find('div', class_='ab-sidebox p-3')

        bookstore = bookstore_container.find('h2').text

        lower_container = soup.find('div', class_='mb-3 small')
        address = lower_container.find('div', class_='flex-grow-1 text-muted').text if lower_container else 'N/A'

        cleaned_address = address.strip()

        final_address_1 = cleaned_address.replace('                    ', ' ')
        final_address_2 = final_address_1.replace('\n', ' ')
        final_address_3 = final_address_2.replace('  ', ',')

        email_container = lower_container.find('div', class_='d-flex mb-2')

        email_child = email_container.find_next_sibling()
        email_child_2 = email_child.find('div', class_='flex-grow-1')

        email = email_child_2.find('a')['href']

        contact_container = email_child.find_next_sibling()

        contact = contact_container.find('div', class_='flex-grow-1 text-muted').text

        por_container = soup.find('div', class_='ab-meta')
        por_child = por_container.find('span')

        por = por_child.find_next_sibling().text

        por_cleaned = por.strip()

        bba_container = soup.find('div', class_='d-flex mb-2')
        
        bba_child1 = bba_container.find('a')

        bba = bba_child1.find_next_sibling()['href']

        bba_url_logic = base_url + bba

        print(bba_url_logic)

        if current_iter == 2:
            break

dealers_url = []

a = dealer_link_harvester(response, dealers_url)

b = extraction(dealers_url)

session.close()
