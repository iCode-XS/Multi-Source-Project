#!/usr/bin/env python3

import pipeline
import showman

# Initiating a session

init = fetch.init_session(fetch.chromium_linux, http2_enable=True)
base_url = 'https://www.boekwinkeltjes.nl'

# Target URL

url = 'https://www.boekwinkeltjes.nl/w/list/'

# Fetching the webiste

website = fetch.fetch_website(init, url, 30)

# Extraction logic begins here


def single_page():

    print()

    parsed = fetch.parse_website(website.text)

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


single_page()
