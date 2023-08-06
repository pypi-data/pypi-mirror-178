#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@File    :   collections.py
@Time    :   2022/11/07 23:33:46
@Author  :   ishtos
@License :   (C)Copyright 2022 ishtos
"""

from .base import BaseAPI


class CollectionsAPI(BaseAPI):
    def list_collections(self, **params):
        endpoint = "/v2/collections"

        return self.request(endpoint, params=params)

    def get_trending_collections(self, **params):
        endpoint = "/v2/collections/trending"

        return self.request(endpoint, params=params)

    def get_collection_by_slug(self, slug, **params):
        endpoint = f"/v2/collections/slug/{slug}"

        return self.request(endpoint, params=params)

    def get_collection(self, address, **params):
        endpoint = f"/v2/collections/{address}"

        return self.request(endpoint, params=params)

    def get_item(self, collection_address, token_id, **params):
        endpoint = f"/v2/collections/{collection_address}/tokens/{token_id}"

        return self.request(endpoint, params=params)

    def get_collection_attribute_values(self, collection_address, trait_type, **params):
        endpoint = f"/v2/collections/{collection_address}/trait-types/{trait_type}/values"

        return self.request(endpoint, params=params)

    def get_collection_attributes(self, collection_address, **params):
        endpoint = f"/v2/collections/{collection_address}/attributes"

        return self.request(endpoint, params=params)
