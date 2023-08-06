#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@File    :   sales.py
@Time    :   2022/11/07 23:39:34
@Author  :   ishtos
@License :   (C)Copyright 2022 ishtos
"""

from .base import BaseAPI


class SalesAPI(BaseAPI):
    def recent_taker_orders_grouped_by_txn_hash(self, **params):
        endpoint = "/v2/sales/recent-taker-orders"

        return self.request(endpoint, params=params)
