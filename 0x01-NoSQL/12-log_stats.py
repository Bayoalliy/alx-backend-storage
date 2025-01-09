#!/usr/bin/env python3
"""Write a Python script that provides some stats about Nginx
logs stored in MongoDB:

Database: logs
Collection: nginx
Display (same as the example):
first line: x logs where x is the number of documents in this collection
second line: Methods:
5 lines with the number of documents with the method =
["GET", "POST", "PUT", "PATCH", "DELETE"] in this order
(see example below - warning: it’s a tabulation before each line)
one line with the number of documents with:
method=GET
path=/status
You can use this dump as data sample: dump.zip
"""
from pymongo import MongoClient


client = MongoClient('mongodb://127.0.0.1:27017')
logs = client.logs.nginx

if __name__ == '__main__':
    print('{} logs'.format(logs.count_documents({})))
    print('Methods:')
    print('    method GET: {}'.format(logs.count_documents({'method': 'GET'})))
    print('    method POST: {}'.format(logs.count_documents({'method': 'POST'})))
    print('    method PUT: {}'.format(logs.count_documents({'method': 'PUT'})))
    print('    method PATCH: {}'.format(logs.count_documents({'method': 'PATCH'})))
    print('    method DELETE: {}'.format(logs.count_documents({'method': 'DELETE'})))
    print('{} status check'.format(logs.count_documents(
    {'method': 'GET', 'path': {'$regex': '/status'}})))
