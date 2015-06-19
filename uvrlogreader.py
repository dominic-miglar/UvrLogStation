#!/usr/bin/env python2

"""
This module contains the UvrLogReader which provides a very high level
layer to communicate with the bootloader.
"""

from UvrSocketIo.uvrconnection import UvrConnection
from serializers import UvrDataSerializer

__author__ = "Dominic Miglar"
__copyright__ = "Copyright 2015"
__license__ = "GPL"
__maintainer__ = "Dominic Miglar"
__email__ = "dominic.miglar@w1r3.net"


class UvrLogReader(object):
    def __init__(self, uvrhost, uvrport):
        self.uvrhost = uvrhost
        self.uvrport = uvrport

    def getData(self):
        '''
        Reads data from UVR, serializes it to JSON and returns it in this format.
        If no data was received from the UVR, this method will return None.
        '''
        uvr_connection = UvrConnection(self.uvrhost, self.uvrport)
        uvr_data = uvr_connection.getData()
        if uvr_data:
            uvr_data_serializer = UvrDataSerializer(uvr_data)
            uvr_data = uvr_data_serializer.serialize()
        else:
            uvr_data = None
        return uvr_data

    def getLatest(self):
        raise NotImplementedError()

    def resetData(self):
        uvr_connection = UvrConnection(self.uvrhost, self.uvrport)
        uvr_connection.resetData()
        return None

