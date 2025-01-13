#!/usr/bin/env python3
"""
Write a Python script that provides some stats about Nginx
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

Improve 12-log_stats.py by adding the top 10 of the most
present IPs in the collection nginx of the database logs
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


def get_top_ips():
    """return top 10 ips"""
    ips = logs.aggregate([
        {
            '$group': {
                '_id': '$ip',
                'num_ip': {'$sum': 1}
            }
        },
        {
            '$sort': {'num_ip': -1}
        },
        {
            '$limit': 10
        }
    ])

    print('IPs:')

    for ip in ips:
        print('\t{}: {}'.format(ip['_id'], ip['num_ip']))


if __name__ == '__main__':
    print_nginx_logs()
    get_top_ips()
