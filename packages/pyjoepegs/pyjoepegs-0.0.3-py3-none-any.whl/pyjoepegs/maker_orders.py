#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@File    :   maker_orders.py
@Time    :   2022/11/07 23:37:40
@Author  :   ishtos
@License :   (C)Copyright 2022 ishtos
"""

from .base import BaseAPI


class MakerOrdersAPI(BaseAPI):
    def list_maker_orders(self, **params):
        endpoint = "/v2/maker-orders"

        return self.request(endpoint, params=params)

    def get_maker_order(self, order_id, **params):
        endpoint = f"/v2/maker-orders/{order_id}"

        return self.request(endpoint, params=params)
