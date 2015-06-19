#!/usr/bin/env python2

"""
This module contains the ResetRequest class which is used to tell the
This module contains the ResetRequest class which is used to tell the
bootloader to clear his data flash.
"""

from constants import *
from uvrerrors import *
from request import Request
import struct

__author__ = "Bertram Winter, Dominic Miglar"
__copyright__ = "Copyright 2015"
__license__ = "GPL"
__maintainer__ = "Dominic Miglar"
__email__ = "dominic.miglar@w1r3.net"

class ResetRequest(Request):
    def __init__(self):
        self.data = struct.pack("B", RESET_DATA)
        self.length = RESET_LENGTH
                
    def finished(self, data):
        if len(data) >= self.length:
            return True
        else:
            return False
        
    def processResponse(self, data):
        if len(data) is not self.length:
            raise UvrResponseError("Invalid Response for EndReadRequest", data)
        
        response = struct.unpack("B", data)[0]
        if response is not RESET_DATA:
            return False
        else:
            return True
        
            