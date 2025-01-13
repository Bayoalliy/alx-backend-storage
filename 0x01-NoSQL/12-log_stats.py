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


def print_nginx_logs():
    """this function prints nginx logs based on request methods"""
    print('{} logs'.format(logs.count_documents({})))
    print('Methods:')
    print('\tmethod GET: {}'.format(logs.count_documents({'method': 'GET'})))
    print('\tmethod POST: {}'.format(logs.count_documents({'method': 'POST'})))
    print('\tmethod PUT: {}'.format(logs.count_documents({'method': 'PUT'})))
    print('\tmethod PATCH: {}'.format(
        logs.count_documents({'method': 'PATCH'})))
    print('\tmethod DELETE: {}'.format(
        logs.count_documents({'method': 'DELETE'})))
    print('{} status check'.format(logs.count_documents(
        {'method': 'GET', 'path': '/status'})))
    print(logs.find_one({'method': 'POST'}))

def get_ips():
    """return top 10 ips"""

if __name__ == '__main__':
    print_nginx_logs()
