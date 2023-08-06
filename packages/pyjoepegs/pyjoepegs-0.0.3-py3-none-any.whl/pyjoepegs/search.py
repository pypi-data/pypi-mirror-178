#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@File    :   search.py
@Time    :   2022/11/07 23:40:28
@Author  :   ishtos
@License :   (C)Copyright 2022 ishtos
"""

from .base import BaseAPI


class SearchAPI(BaseAPI):
    def search(self, **params):
        endpoint = "/v2/search"

        return self.request(endpoint, params=params)
