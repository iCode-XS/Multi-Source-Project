#!/usr/bin/env python3

from core import pipeline
from core import showman

# Initiating a session

init = pipeline.init_session(pipeline.chromium_linux, http2_enable=True)
base_url = 'https://www.boekwinkeltjes.nl'

# Target URL

url = 'https://www.boekwinkeltjes.nl/w/list/'

# Fetching the webiste

website = pipeline.fetch_website(init, url, 30)

# Extraction logic begins here


def single_page(response_var):

    print()

    parsed = pipeline.parse_website(response_var)

    table = parsed.find('table')

    tr = table.find_all('tr')

    for x in tr:

        capture = {}

        image_url_cont = x.find('td')
        author_url = image_url_cont.find('a') if image_url_cont else None
        image_url = author_url.find('img')['src'] if author_url else 'N/A'

        if 'https://images.boekwinkeltjes.nl' in image_url:
            capture['Image Source'] = image_url

        elif 'https://img.boekwinkeltjes.nl' in image_url:
            capture['Image Source'] = image_url

        elif base_url in image_url:
            capture['Image Source'] = image_url

        elif 'N/A' in image_url:
            capture['Image Source'] = image_url

        else:
            capture['Image Source'] = base_url + image_url

        # print(image_url)

        bookstore_cont = image_url_cont.find_next_sibling() if image_url_cont else None
        capture['Bookstore'] = bookstore_cont.text.strip() if bookstore_cont else 'N/A'


        por = bookstore_cont.find_next_sibling() if bookstore_cont else None
        capture['Place of Residence'] = por.text.strip() if por else 'N/A'

        books = por.find_next_sibling() if por else None
        books_a = books.find('a')['href'] if books else None
        capture['Books by Author'] = base_url + books_a if books_a else 'N/A'

        contact_container = books.find_next_sibling() if books else None
        contact_a = contact_container.find('a')['href'] if contact_container else None
        capture['Contact Source'] = base_url + contact_a if contact_a else 'N/A'

        showman.carriage_dict(capture, timeout=0.7)

        print(f'\r{showman.MOVE_UP}{showman.CLEAR_LINE}')


    next_page_sibling = parsed.find('i', class_='fa fa-arrow-right')
    next_page_link = next_page_sibling.parent['href'] if next_page_sibling else None

    next_page = base_url + next_page_link if next_page_link else None

    return next_page

def multi_page(single_page_var):

    current_url = ''

    current_url = single_page_var

    while current_url:

        next_response = pipeline.fetch_website(init, current_url, 30)

        parsed1 = single_page(next_response)

        current_url = parsed1

page_1 = single_page(website)
multi_page(page_1)
