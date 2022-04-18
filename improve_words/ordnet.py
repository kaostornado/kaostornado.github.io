import requests
from requests.adapters import HTTPAdapter
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import math
from urllib3 import Retry
import numpy as np
import time
import random

from initial_words import words


# Current problem:
# IP gets blocked by ordnet.dk
# Solutions: https://understandingdata.com/how-to-avoid-being-blocked-web-scraping/


# When making many requests, it is a good idea to use a session.
# This will improve performance significantly by using connection pooling
session = requests.Session()
http_proxy = os.getenv('http_proxy')
https_proxy = os.getenv('https_proxy')

# Recommended number of workers
NUM_WORKERS = os.cpu_count() * 5

def word_exists(word: str) -> bool:
    """ Returns true if the word is in the Danish dictionary.
        You should probably use proxies for this. Ordnet will block
        your IP address otherwise. I use a paid proxy service called packetstream.io.
        It uses a new proxy for every request.
        If you don't want to pay, you can experiment with increasing
        the sleep time between each request and lowering
        the number of workers. """

    if 'at være ' in word:
        word = word.replace('at være ', '')

    status_code = 0
    try:
        res = ordnet_request(word)
        status_code = res.status_code
    except requests.exceptions.ConnectionError:
        status_code = "CONNECTION REFUSED"

    print(status_code, word)
    time.sleep(random.randint(0, 3))
    return status_code == 200
    

def ordnet_request(word):
    url = 'https://ordnet.dk/ddo/ordbog?query=' + word
    proxies = {
        "http": http_proxy,
        "https": https_proxy,
    }
    res = session.get(
        url, 
        proxies=proxies
    )
    return res


def split_work(words=words, num_workers=NUM_WORKERS):
    """ The list of words is very long 
        and we need to make a request for each one.
        This function makes num_workers intervals that can be
        used by a ThreadPoolExecutor """
    nd_array_list = np.array_split(words, num_workers)
    return [nd_array.tolist() 
            for nd_array
            in nd_array_list]


def do_work(chunk: list[str]) -> list[str]:
    new_words = []
    for word in chunk:
        if word_exists(word):
            new_words.append(word)
    return new_words
    


def words_that_exist(words: list[str]) -> list[str]:
    """ Returns words that are in the Danish dictionary """
    new_words = []
    chunks = split_work(words)

    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        futures = []
        for chunk in chunks:
            futures.append(
                executor.submit(do_work, chunk)
            )
        for future in as_completed(futures):
            new_words.extend(future.result())
    
    return new_words