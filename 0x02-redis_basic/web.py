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
import requests


r = redis.Redis()


def get_page(url: str) -> str:
    """obtain the HTML content of a particular URL and returns it"""
    if r.get(url):
        r.incr(f"count:{url}")
        return r.get(url)

    res = requests.get(url)
    r.set(f"cached:{url}", str(res), ex=30)
    r.expire(f"cached:{url}")
    r.incr(f"count:{url}")
    return res.text


if __name__ == '__main__':
    get_page('http://slowwly.robertomurray.co.uk')
