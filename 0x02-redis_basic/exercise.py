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
from typing import Union, Callable
from functools import wraps


def call_history(method: Callable) -> Callable:
    """decorator function storing call history"""
    @wraps(method)
    def wrapper_fun(self, *args, **kwargs):
        """wrapper function"""
        inputs_key = method.__qualname__ + ':inputs'
        outputs_key = method.__qualname__ + ':outputs'
        self._redis.rpush(inputs_key, str(args))
        res = method(self, *args, **kwargs)
        self._redis.rpush(outputs_key, res)
        return res
    return wrapper_fun


def count_calls(method: Callable) -> Callable:
    """decorator function"""
    @wraps(method)
    def wrapper_func(self, *args, **kwargs):
        """wrapper function"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper_func


def replay(method):
    """display the history of calls of a particular function"""
    r = redis.Redis()
    num_calls = r.get(method.__qualname__).decode('utf-8')
    inputs = r.lrange(method.__qualname__ + ":inputs", 0, -1)
    outputs = r.lrange(method.__qualname__ + ":outputs", 0, -1)
    print(f"{method.__qualname__} was called {num_calls} times")

    for key, value in zip(outputs, inputs):
        k = key.decode('utf-8')
        v = value.decode('utf-8')
        print(f"{method.__qualname__}(*{v}) -> {k}")


class Cache:
    """Cahindg class"""
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
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
