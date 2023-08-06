#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@File    :   users.py
@Time    :   2022/11/07 23:41:20
@Author  :   ishtos
@License :   (C)Copyright 2022 ishtos
"""

from .base import BaseAPI


class UsersAPI(BaseAPI):
    def get_user_by_name(self, name, **params):
        endpoint = f"/v2/users/name/{name}"

        return self.request(endpoint, params=params)

    def get_user(self, address, **params):
        endpoint = f"/v2/users/{address}"

        return self.request(endpoint, params=params)

    def get_user_collections(self, address, **params):
        endpoint = f"/v2/users/{address}/collections"

        return self.request(endpoint, params=params)

    def get_user_items(self, address, **params):
        endpoint = f"/v2/users/{address}/items"

        return self.request(endpoint, params=params)

    def get_user_items_on_auction(self, address, **params):
        endpoint = f"/v2/users/{address}/auction-items"

        return self.request(endpoint, params=params)

    def get_user_bids_received(self, address, **params):
        endpoint = f"/v2/users/{address}/bids-received"

        return self.request(endpoint, params=params)

    def get_user_activity(self, address, **params):
        endpoint = f"/v2/users/{address}/activity"

        return self.request(endpoint, params=params)
