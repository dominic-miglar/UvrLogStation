#!/usr/bin/env python2

"""
This module contains the HeaderRequest and HeaderResponse classes which are
used to get various information on how the logged data is saved in the
bootloader's data flash.
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

VALID_HEADER_LENGTHS = [CAN_HEADER_LENGTH, DL_HEADER_LENGTH, DL2_HEADER_LENGTH]

def isValidAddress(a):
    return not(a[2] is 0xFF and a[1] is 0xFF and a[0] is 0xFF)
        
def fixAddress(a):
    return (a[2]<<15) + (a[1]<<7) + a[0]

class HeaderRequest(Request):    
    def __init__(self, mode):
        self.data = struct.pack("B", GET_HEADER)
        self.mode = mode
        self.length = max(VALID_HEADER_LENGTHS)
        
    def finished(self, data):
        if len(data) >= min(VALID_HEADER_LENGTHS):
            return True
        else:
            return False
        
    def processResponse(self, data):
        if not self.validateChecksum(data):
            raise UvrChecksumError("Checksum error for HeaderRequest", data)
        return HeaderResponse(data, self.mode)

            
class HeaderResponse(object):
    def __init__(self, data, mode):  
        binary = struct.unpack(len(data)*"B", data)          
        if mode is CAN_MODE:
            frames = binary[5]
            index = 6 + frames
            size = 64 * frames
        elif mode is DL_MODE:
            frames = 1
            index = 7
            size = 64
        elif mode is DL2_MODE:
            frames = 1
            index = 8
            size = 128
            
        startAddress = binary[index:index+3]
        endAddress = binary[index+3:index+6]
            
        if (isValidAddress(startAddress) and
           isValidAddress(endAddress)):
            start = fixAddress(startAddress)
            end = fixAddress(endAddress)
            address = end
            if end > start:
                count = 1 + (end - start) / size
            else:
                count = (MAX_ADDRESS - end + start) / size
        else:
            count = 0
            address = 0

        self.frames = frames
        self.count = count
        self.address = address
        self.size = size
        
    def getAddresses(self):
        for i in range(self.count):
            yield self.address
            self.address -= self.size
            if self.address < 0:
                self.address = int(MAX_ADDRESS/self.size)*self.size
            
            