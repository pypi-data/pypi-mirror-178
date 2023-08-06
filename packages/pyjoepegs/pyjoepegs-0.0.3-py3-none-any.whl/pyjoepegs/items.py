#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@File    :   items.py
@Time    :   2022/11/07 23:35:03
@Author  :   ishtos
@License :   (C)Copyright 2022 ishtos
"""

from .base import BaseAPI


class ItemsAPI(BaseAPI):
    def list_items(self, **params):
        endpoint = "/v2/items"

        return self.request(endpoint, params=params)
