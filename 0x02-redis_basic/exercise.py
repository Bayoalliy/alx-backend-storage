#!/usr/bin/env python3
"""
Create a Cache class. In the __init__ method, store an instance
of the Redis client as a private variable named _redis
(using redis.Redis()) and flush the instance using flushdb.

Create a store method that takes a data argument and returns a string.
The method should generate a random key (e.g. using uuid),
store the input data in Redis using the random key and return the key.

Type-annotate store correctly.
Remember that data can be a str, bytes, int or float.
"""

import redis
import uuid
from typing import Union
from functools import wraps


def count_calls(Callable):
    """decorator function"""
    @wraps(Callable)
    def wrapper_func(self, *args, **kwargs):
        """wrapper function"""
        key = Callable.__qualname__
        self._redis.incrby(key, 1)
        return Callable(self, *args, **kwargs)
    return wrapper_func


class Cache:
    """Cahindg class"""
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """stores data in redis database"""
        u_id = str(uuid.uuid4())
        self._redis.set(u_id, data)
        return u_id

    def get(self, key, fn=None):
        """gets a value from redis db using its key"""
        res = self._redis.get(key)
        if fn:
            res = fn(res)
        return res

    def get_int(self, key):
        """parameterize get with int function"""
        return self.get(key, int)

    def get_str(self, key):
        """parameterize get with string function"""
        def fn(d): d.decode("utf-8")
        return self.get(key, fn)
