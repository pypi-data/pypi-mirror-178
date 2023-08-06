#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@File    :   activities.py
@Time    :   2022/11/07 23:31:51
@Author  :   ishtos
@License :   (C)Copyright 2022 ishtos
"""

from .base import BaseAPI


class ActivitiesAPI(BaseAPI):
    def list_activity_by_collection(self, collection_address, **params):
        endpoint = f"/v2/activities/{collection_address}"

        return self.request(endpoint, params=params)

    def list_activity_by_item(self, collection_address, token_id, **params):
        endpoint = f"/v2/activities/{collection_address}/tokens/{token_id}"

        return self.request(endpoint, params=params)
