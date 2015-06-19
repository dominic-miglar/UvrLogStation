#!/usr/bin/env python2

"""
This module contains the LatestRequest and LatestResponse classes which are
used to get the current values out of the heating controller.
"""

from constants import *
from uvrerrors import *
from request import Request
from parser import Parser
import struct

__author__ = "Bertram Winter, Dominic Miglar"
__copyright__ = "Copyright 2015"
__license__ = "GPL"
__maintainer__ = "Dominic Miglar"
__email__ = "dominic.miglar@w1r3.net"

class LatestRequest(Request):    
    def __init__(self, mode, frame):
        self.data = struct.pack("BB", GET_LATEST, frame+1)
        self.mode = mode
        if self.mode is CAN_MODE:
            self.length = CAN_LATEST_LENGTH
        elif self.mode is DL_MODE:
            self.length = DL_LATEST_LENGTH
        elif self.mode is DL2_MODE:
            self.length = DL2_LATEST_LENGTH
        
    def finished(self, data):
        if len(data) is self.length:
            return True
        else:
            if len(data) is WAIT_LENGTH and self.validateChecksum(data):
                cmd, timeout = struct.unpack("BB", data[0:2])
                if cmd is WAIT_TIME:
                    raise UvrWait("UVR busy", timeout)
            return False
        
    def processResponse(self, data):
        if not self.validateChecksum(data):
            raise UvrChecksumError("Checksum error for HeaderRequest", data)
        return LatestResponse(data, self.mode)

            
class LatestResponse(object):
    def __init__(self, data, mode):
        self.datasets = []
        parser = Parser()
        if mode is CAN_MODE:
            self.datasets.append(parser.parseDataset(data[1:56]))
        elif mode is DL_MODE:
            self.datasets.append(parser.parseDataset(data[1:56]))
        elif mode is DL2_MODE:
            self.datasets.append(parser.parseDataset(data[1:56]))
            self.datasets.append(parser.parseDataset(data[57:112]))