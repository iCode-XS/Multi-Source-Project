#!/usr/bin/env python3

import httpx
from loguru import logger
from bs4 import BeautifulSoup
import pandas as pd


# logger.remove()

logger.add('event.log', rotation='10MB')


chromium_linux = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chromium/133.0.0.0 Chrome/133.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive"
}


def init_session(current_header, http2_enable=False):

    logger.info('Trying to create a session...')
    current_session = httpx.Client(headers=current_header, http2=http2_enable)
    logger.info('Success! Current session has been created')

    return current_session


@logger.catch
def fetch_website(session_name, url, timer, http2_enable=False):

    try:
        logger.info('Trying to send GET Request...')
        response = session_name.get(url, timeout=timer)
        response.raise_for_status()
        logger.info(f'GET Request success! URL: {response.url}')
        logger.info(f'Status Code: {response.status_code}')

        return response

    except httpx.HTTPStatusError as e:
        raise RuntimeError(f'Something is wrong with the GET Request {e.response.url} | {e.response.status_code}')


@logger.catch
def parse_website(response_object):

    try:
        logger.info('Trying to parse the bs4 object...')
        soup = BeautifulSoup(response_object, 'lxml')
        logger.info('Success! The BeautifulSoup Object has been parsed successfully')

        return soup

    except Exception as e:
        raise RuntimeError(f'Something is wrong in parsing the bs4 object: {response_object}', e)

def load_data(payload, name, save_csv=False, save_excel=False, index_switch=False, append=False, headers_on=False):

    try:
        data = pd.DataFrame(payload)

        if save_csv:
            data.to_csv(name, index=index_switch, mode='a' if append else 'w', header=headers_on)

        if save_excel:
            data.to_excel(name, index=index_switch)

    except Exception:
        raise RuntimeError(f'There is something wrong with the {payload} data structure')
