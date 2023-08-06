#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@File    :   pyjoepegs.py
@Time    :   2022/11/07 23:29:38
@Author  :   ishtos
@License :   (C)Copyright 2022 ishtos
"""
from .activities import ActivitiesAPI
from .collections import CollectionsAPI
from .items import ItemsAPI
from .maker_orders import MakerOrdersAPI
from .owners import OwnersAPI
from .sales import SalesAPI
from .search import SearchAPI
from .users import UsersAPI


class JoepegsAPI:
    def __init__(self, api_key, timeout=None):
        self.api_key = api_key
        self.timeout = timeout

    def singleton(self, attribute_name, cls):
        if hasattr(self, attribute_name):
            instance = getattr(self, attribute_name)
            return instance

        instance = cls(self.api_key, self.timeout)
        setattr(self, attribute_name, instance)
        return instance

    def activities(self):
        return self.singleton("_activities", ActivitiesAPI)

    def collections(self):
        return self.singleton("_collections", CollectionsAPI)

    def items(self):
        return self.singleton("_items", ItemsAPI)

    def maker_orders(self):
        return self.singleton("_maker_orders", MakerOrdersAPI)

    def owners(self):
        return self.singleton("_owners", OwnersAPI)

    def sales(self):
        return self.singleton("_sales", SalesAPI)

    def search(self):
        return self.singleton("_search", SearchAPI)

    def users(self):
        return self.singleton("_users", UsersAPI)
