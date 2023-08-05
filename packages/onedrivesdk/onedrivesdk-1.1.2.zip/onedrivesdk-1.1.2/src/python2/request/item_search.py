# -*- coding: utf-8 -*- 
'''
# Copyright (c) 2015 Microsoft Corporation
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# 
#  This file was generated and any changes will be overwritten.
'''

from ..model.item import Item
from ..collection_base import CollectionRequestBase
from ..request_builder_base import RequestBuilderBase
from ..options import *
import json


class ItemSearchRequest(CollectionRequestBase):

    def __init__(self, request_url, client, options, q=None):
        super(ItemSearchRequest, self).__init__(request_url, client, options)
        self.method = "GET"

        if q:
            self._query_options["q"] = q

    def get(self):
        """Sends the GET request
        
        Returns:
            :class:`ItemsCollectionResponse<onedrivesdk.request.items_collection.ItemsCollectionResponse>`:
                The resulting collection page from the operation
        """
        collection_response = ItemsCollectionResponse(json.loads(self.send().content))
        return self._page_from_response(collection_response)



class ItemSearchRequestBuilder(RequestBuilderBase):

    def __init__(self, request_url, client, q=None):
        super(ItemSearchRequestBuilder, self).__init__(request_url, client)
        self._method_options = {}

        self._method_options["q"] = q

    def request(self, expand=None, select=None, top=None, order_by=None, options=None):
        """Builds the request for the ItemSearch
        
        Args:
            expand (str): Default None, comma-seperated list of relationships
                to expand in the response.
            select (str): Default None, comma-seperated list of properties to
                include in the response.
            top (int): Default None, the number of items to return in a result.
            order_by (str): Default None, comma-seperated list of properties
                that are used to sort the order of items in the response.
            options (list of :class:`Option<onedrivesdk.options.Option>`):
                Default to None, list of options to include in the request

        Returns: 
            :class:`ItemSearchRequest<onedrivesdk.request.item_search.ItemSearchRequest>`:
                The request
        """
        req = ItemSearchRequest(self._request_url, self._client, options, q=self._method_options["q"])
        req._set_query_options(expand=expand, select=select, top=top, order_by=order_by)
        return req

    def get(self):
        """Sends the GET request
        
        Returns:
            :class:`ItemsCollectionResponse<onedrivesdk.request.items_collection.ItemsCollectionResponse>`:
            The resulting ItemsCollectionResponse from the operation
        """
        return self.request().get()

from ..request.items_collection import ItemsCollectionResponse
