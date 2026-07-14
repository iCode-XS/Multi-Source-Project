#!/usr/bin/env python3

from core import pipeline

base_url = 'https://www.pbfa.org'

target_url = 'https://www.pbfa.org/members'

session = pipeline.init_session(pipeline.chromium_linux)

response = pipeline.fetch_website(session, target_url, timer=20)

soup = pipeline.parse_website(response)
