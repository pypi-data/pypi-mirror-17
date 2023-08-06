# Copyright (c) 2013 Alon Swartz <alon@turnkeylinux.org>
#
# This file is part of OctoHub.
#
# OctoHub is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.

import requests
import json
from hexahub import __useragent__
from hexahub.response import parse_response


class Pager(object):
    def __init__(self, conn, uri, params, max_pages=0):
        """Iterator object handling pagination of Connection.send (method: GET)
            conn (hexahub.Connection): Connection object
            uri (str): Request URI (e.g., /user/issues)
            params (dict): Parameters to include in request
            max_pages (int): Maximum amount of pages to get (0 for all)
        """
        self.conn = conn
        self.uri = uri
        self.params = params
        self.max_pages = max_pages
        self.count = 0

    def __iter__(self):
        while True:
            self.count += 1
            response = self.conn.send('GET', self.uri, self.params)
            yield response

            if self.count == self.max_pages:
                break

            if not 'next' in response.parsed_link.keys():
                break


            # I don't know why, but parsing the next link provides really bad result here
            next_link = response.links['next']['url']
            count_endpoint = len(self.conn.endpoint)
            self.uri = next_link[count_endpoint:]


class Connection(object):
    logger = None

    def __init__(self, token=None, endpoint=None, logger=None):
        """OctoHub connection
            token (str): GitHub Token (anonymous if not provided)
            endpoint (str): Github Enterprise API Endpoint (Github official if not provided)
            logger (object): lggr instance
        """
        if endpoint:
            self.endpoint = endpoint
        else:
            self.endpoint = 'https://api.github.com'
        self.headers = {'User-Agent': __useragent__}

        if token:
            self.headers['Authorization'] = 'token %s' % token

        if logger:
            self.logger = logger

    def send(self, method, uri, params={}, data=None):
        """Prepare and send request
            method (str): Request HTTP method (e.g., GET, POST, DELETE, ...)
            uri (str): Request URI (e.g., /user/issues)
            params (dict): Parameters to include in request
            data (str | file type object): data to include in request

            returns: requests.Response object, including:
                response.parsed (AttrDict): parsed response when applicable
                response.parsed_link (AttrDict): parsed header link when applicable
                http://docs.python-requests.org/en/latest/api/#requests.Response
        """
        url = self.endpoint + uri
        if self.logger:
            self.logger.debug("Request: %s %s with %s" % (method, url, json.dumps(params, sort_keys=True,
                                                                                  indent=2, separators=(',', ': '))))
        kwargs = {'headers': self.headers, 'params': params, 'data': data}
        response = requests.request(method, url, **kwargs)

        return parse_response(response)
