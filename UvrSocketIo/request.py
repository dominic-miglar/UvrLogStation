#!/usr/bin/env python2

"""
This module contains the Request class which is the base class for all
other requests and provides some checksum validation operations
"""

import logging
import struct

__author__ = "Bertram Winter, Dominic Miglar"
__copyright__ = "Copyright 2015"
__license__ = "GPL"
__maintainer__ = "Dominic Miglar"
__email__ = "dominic.miglar@w1r3.net"

logger = logging.getLogger(__name__)

class Request(object):
    def __init__(self):
        pass
        
    def validateChecksum(self, data):
        checksum1 = self.checksum(data[0:-1])
        checksum2 = struct.unpack("B", data[-1])
        # fix of checksum 2, extract checksum from tuple
        checksum2 = checksum2[0]
        if checksum1 == checksum2:
            logger.debug('CHECKSUM OK!')
        else:
            logger.debug('CHECKSUM ERROR!')
        return checksum1 == checksum2
        
    def addChecksum(self, data):
        checksum = self.checksum(data)
        data += struct.pack("B", checksum)
        return data
        
    def checksum(self, data):
        bytes = struct.unpack(len(data)*"B", data)
        sum = 0
        for byte in bytes:
            sum += byte
        return sum & 0xFF