#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@File    :   owners.py
@Time    :   2022/11/07 23:38:40
@Author  :   ishtos
@License :   (C)Copyright 2022 ishtos
"""

from .base import BaseAPI


class OwnersAPI(BaseAPI):
    def list_owners(self, **params):
        endpoint = "/v2/owners"

        return self.request(endpoint, params=params)

    def list_collection_owners(self, collection_id, **params):
        endpoint = f"/v2/owners/collections/{collection_id}"

        return self.request(endpoint, params=params)
