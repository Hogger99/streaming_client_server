#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import requests


def run_request():

    # change this to be the actual url for the REST endpoint
    microservice_url = 'http://localhost:9999/api/vi/query_data'
    params = {'key': 'name',
              'value': 'george'
              }

    headers = {'Content-Type': 'application/json'}

    records = []
    error = None
    r = requests.get(url=microservice_url, params=params, headers=headers)
    if r.status_code == 200:
        records = r.json()
    else:
        error = r.text
    
    return records, error


if __name__ == '__main__':
    # get command line parameters here

    records, error = run_request()

