#!/usr/bin/env python2

"""
This module contains the ModeRequest class, which is used to get
information about in what (logging) mode the bootloader resides.
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

class ModeRequest(Request):
    def __init__(self):
        self.data = struct.pack("B", GET_MODE)
        self.length = MODE_LENGTH
                
    def finished(self, data):
        if len(data) >= self.length:
            return True
        else:
            return False
        
    def processResponse(self, data):
        if len(data) is not self.length:
            raise UvrResponseError("Invalid Response for ModeRequest", data)
        
        mode = struct.unpack("B", data)[0]
        if mode not in [CAN_MODE, DL_MODE, DL2_MODE]:
            raise  UvrModeError("Mode not supported: 0x%02X" % mode)
        return mode
        
            
