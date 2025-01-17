#!/usr/bin/env python3
"""
In this tasks, we will implement a get_page
function (prototype: def get_page(url: str) -> str:).
The core of the function is very simple. It uses the requests
module to obtain the HTML content of a particular URL and returns it.

Start in a new file named web.py and do not
reuse the code written in exercise.py.

Inside get_page track how many times a particular URL was
accessed in the key "count:{url}" and cache the result
with an expiration time of 10 seconds.

Tip: Use http://slowwly.robertomurray.co.uk to simulate a
slow response and test your caching.
"""
import redis
from typing import Union, Callable
import requests


def get_page(url: str) -> str:
    """obtain the HTML content of a particular URL and returns it"""
    r = redis.Redis()
    if r.get(url):
        r.incr(f"count:{url}")
        return r.get(url)

    res = requests.get(url)
    r.set(url, str(res), ex=10)
    r.incr(f"count:{url}")
    return res
