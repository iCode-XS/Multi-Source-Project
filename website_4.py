#!/usr/bin/env python3

from core import pipeline


target_url = 'https://www.ioba.org/members-directory'

session = pipeline.init_session(pipeline.chromium_linux)

response = pipeline.fetch_website(session, target_url, timer=20)

parsed = pipeline.parse_website(response)

container = parsed.find_all('div', class_='_FiCX')

for x in container:

    title = x.find('span', class_='wixui-rich-text__text', style='font-weight:bold;').text

    contact = x.find('span', class_='wixui-rich-text__text', style='font-size:14px;').text
