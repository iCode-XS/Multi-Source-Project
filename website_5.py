#!/usr/bin/env python3

from core import pipeline

target_url = 'https://nvva.nl/en/members/'

session = pipeline.init_session(pipeline.chromium_linux)

response = pipeline.fetch_website(session, target_url, timer=20)

parsed = pipeline.parse_website(response)
