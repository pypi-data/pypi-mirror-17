# Copyright (c) 2013 Alon Swartz <alon@turnkeylinux.org>
#
# This file is part of OctoHub.
#
# OctoHub is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.

import re
import pprint
import urlparse

from hexahub.utils import AttrDict, get_logger
from hexahub.exceptions import ResponseError, OctoHubError

log = get_logger('response')

def _get_content_type(response):
    """Parse response and return content-type"""
    try:
        content_type = response.headers['Content-Type']
        content_type = content_type.split(';', 1)[0]
    except KeyError:
        content_type = None

    return content_type

def _parse_link(response):
    """Parse header link and return AttrDict[rel].uri|params"""
    header_link = response.headers['link']
    links = AttrDict()
    for s in header_link.split(','):
        link = AttrDict()

        parsed_url = urlparse.urlparse(response.url)
        regex = "<%s://%s(.*)\?(.*)>" % (parsed_url.scheme, parsed_url.netloc)
        m = re.match(regex, s.split(';')[0].strip())
        link.uri = m.groups()[0]
        link.params = {}
        for kv in m.groups()[1].split('&'):
            key, value = kv.split('=')
            link.params[key] = value

        m = re.match('rel="(.*)"', s.split(';')[1].strip())
        rel = m.groups()[0]

        links[rel] = link
        log.debug('link-%s-page: %s' % (rel, link.params['page']))

    return links

def parse_element(el):
    """Parse el recursively, replacing dicts with AttrDicts representation"""
    if type(el) == dict:
        el_dict = AttrDict()
        for key, val in el.items():
            el_dict[key] = parse_element(val)

        return el_dict

    elif type(el) == list:
        el_list = []
        for l in el:
            el_list.append(parse_element(l))

        return el_list

    else:
        return el

def parse_response(response):
    """Parse request response object and raise exception on response error code
        response (requests.Response object):

        returns: requests.Response object, including:
            response.parsed (AttrDict)
            response.parsed_link (AttrDict)
            http://docs.python-requests.org/en/latest/api/#requests.Response
    """
    response.parsed = AttrDict()
    response.parsed_link = AttrDict()

    if 'link' in response.headers.keys():
        response.parsed_link = _parse_link(response)

    headers = ['status', 'x-ratelimit-limit', 'x-ratelimit-remaining']
    for header in headers:
        if header in response.headers.keys():
            log.info('%s: %s' % (header, response.headers[header]))

    content_type = _get_content_type(response)

    if content_type == 'application/json':
        json = response.json
        if callable(json):
            json = json()
        response.parsed = parse_element(json)
    else:
        if not response.status_code == 204:
            raise OctoHubError('unhandled content_type: %s' % content_type)

    if not response.status_code in (200, 201, 204):
        raise ResponseError(response.parsed)

    return response


