#!/usr/bin/env python2

"""
This module contains the UvrLogSysClient which is used to communicate with
the backend server (UvrLogSysBackend).
"""

import requests

__author__ = "Dominic Miglar"
__copyright__ = "Copyright 2015"
__license__ = "GPL"
__maintainer__ = "Dominic Miglar"
__email__ = "dominic.miglar@w1r3.net"

class UvrLogClient(object):
    def __init__(self, backend_url, controller_name, username=None, password=None):
        self.backend_url = backend_url
        if self.backend_url[-1] != '/':
            self.backend_url += '/'
        self.controller_name = controller_name
        self.username = username
        self.password = password
        self.http_headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        self.controller_id = None

    def getControllerId(self):
        http_get_params = {'name': self.controller_name}
        query_url = self.backend_url + 'controllers/'
        http_response = requests.get(query_url, params=http_get_params, headers=self.http_headers)
        if(http_response.status_code != requests.codes.ok):
            raise UvrResponseError(message='An error occurred while getting the controller id.',
                response_code = http_response.status_code, response_text=http_response.text)
        if not http_response.json():
            raise UvrControllerDoesNotExistError(message='Controller with name %s does not exist at backend!' %
                self.controller_name)
        controller = http_response.json()[0]
        self.controller_id = controller['id']
        return self.controller_id

    def postUvrData(self, uvr_data):
        if self.controller_id is None:
            self.getControllerId()
        post_url = '%scontrollers/%d/import_data/' % (self.backend_url, self.controller_id)
        http_response = requests.post(post_url, uvr_data, headers=self.http_headers)
        if(http_response.status_code != requests.codes.ok):
            raise UvrResponseError(message='An error occurred while posting the logged data',
                response_code = http_response.status_code, response_text=http_response.text)
        return True


class UvrLogError(Exception):
    pass

class UvrControllerDoesNotExistError(UvrLogError):
    def __init__(self, message):
        self.message = message
        super(UvrControllerDoesNotExistError, self).__init__(message)


class UvrResponseError(UvrLogError):
    def __init__(self, message, response_code, response_text):
        self.message = message
        self.response_code = response_code
        self.response_text = response_text
        super(UvrResponseError, self).__init__(message)
