#!/usr/bin/env python3
"""5. Implement expiring web cache and tracker"""
import requests
import redis


def get_page(url: str) -> str:
    """Return the URL of a web page and track number of visits
    with an expiration of 10 seconds"""
    response = requests.get(url)
    r = redis.Redis()
    count = r.incr("count:{url}")
    r.expire("count:{url}", 10)
    return response.text


if __name__ == '__main__':
    url = "http://google.com"
    page = get_page(url)
    r = redis.Redis()
    print('Visited: ', int(r.get("count:{url}")))
