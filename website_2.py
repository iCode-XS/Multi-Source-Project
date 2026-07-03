#!/usr/bin/env python3

from core import pipeline

base_url = 'https://www.antiqbook.com'

target_website = 'https://www.antiqbook.com/dealers'

session = pipeline.init_session(pipeline.chromium_linux)

response = pipeline.fetch_website(session, target_website, timer=20)


def change_page(response_object):

    soup = pipeline.parse_website(response_object)

    next_page = soup.find('a', class_='page-link', rel='next')['href']

    link_logic = base_url + next_page

    return link_logic


def single_page(response_object):

    soup = pipeline.parse_website(response_object)

    container = soup.find_all('div', style='flex:1;min-width:0;')

    for item in container:

        dealer_name = item.find('a').text
        print('Dealer Name:', dealer_name.strip())


a = single_page(response)
