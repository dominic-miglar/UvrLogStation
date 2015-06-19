#!/usr/bin/env python2

"""
This module contains the UvrConnection class which provides
a high level layer to the bootloader's functionality.
"""

from uvrsocket import UvrSocket
from headerrequest import HeaderRequest
from moderequest import ModeRequest
from latestrequest import LatestRequest
from readrequest import ReadRequest
from endreadrequest import EndReadRequest
from resetrequest import ResetRequest
from firmwarerequest import FirmwareRequest
from uvrerrors import UvrWait
import time

__author__ = "Bertram Winter, Dominic Miglar"
__copyright__ = "Copyright 2015"
__license__ = "GPL"
__maintainer__ = "Dominic Miglar"
__email__ = "dominic.miglar@w1r3.net"

class UvrConnection(object):
    def __init__(self, host, port):
        self.socket = UvrSocket(host, port)
        self.mode = self.getMode()
        self.frames = self.getHeader().frames
    
    def getMode(self):
        self.socket.connect()
        mode = self.socket.request(ModeRequest())
        self.socket.close()
        return mode
        
    def getLatest(self):
        latest = []
        self.socket.connect()
        for i in range(self.frames):
            try:
                latest += self.socket.request(LatestRequest(self.mode, i)).datasets
            except UvrWait as e:
                self.socket.close()
                time.sleep(e.timeout)
                self.socket.connect()
                latest += self.socket.request(LatestRequest(self.mode, i)).datasets
        self.socket.close()
        return latest
        
    def getHeader(self):
        self.socket.connect()
        header = self.socket.request(HeaderRequest(self.mode))
        self.socket.close()
        return header
        
    def getData(self):
        data = []
        header = self.getHeader()
        self.socket.connect()
        for address in header.getAddresses():
            data.append(self.socket.request(ReadRequest(address, self.mode, header.frames)).datasets)
        self.socket.request(EndReadRequest())
        self.socket.close()
        return data
        
    def resetData(self):
        self.socket.connect()
        self.socket.request(ResetRequest())
        self.socket.close()

    def getFirmware(self):
        self.socket.connect()
        firmware = self.socket.request(FirmwareRequest())
        self.socket.close()
        return firmware

