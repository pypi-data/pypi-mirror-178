#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@File    :   baes.py
@Time    :   2022/11/07 23:26:17
@Author  :   ishtos
@License :   (C)Copyright 2022 ishtos
"""

import requests


class BaseAPI:
    def __init__(self, api_key, timeout=None):
        self.api_url = "https://api.joepegs.dev"
        self.api_key = api_key
        self.timeout = timeout

    def request(self, endpoint, params=None):
        url = self.api_url + endpoint
        headers = {
            "Accept": "application/json",
            "x-joepegs-api-key": self.api_key,
        }

        try:
            with requests.Session() as s:
                s.headers.update(headers)
                response = s.get(url, params=params, timeout=self.timeout)
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            # TODO: handle exception
            raise e

        return response.json()
