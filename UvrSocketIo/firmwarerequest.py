#!/usr/bin/env python2

"""
This module contains the FirmwareRequest class which is used to
retrieve the firmware version of the bootloader.
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

class FirmwareRequest(Request):
    def __init__(self):
        self.data = struct.pack("B", GET_FIRMWARE)
        self.length = FIRMWARE_LENGTH
                
    def finished(self, data):
        if len(data) >= self.length:
            return True
        else:
            return False
        
    def processResponse(self, data):
        if len(data) is not self.length:
            raise UvrResponseError("Invalid Response for FirmwareRequest", data)

        firmware = struct.unpack("B", data)[0]
        return firmware
        
