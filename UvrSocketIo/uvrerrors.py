#!/usr/bin/env python2

"""
This module contains error classes (Exceptions) which are raised in other
parts of this library.
"""

import struct

__author__ = "Bertram Winter, Dominic Miglar"
__copyright__ = "Copyright 2015"
__license__ = "GPL"
__maintainer__ = "Dominic Miglar"
__email__ = "dominic.miglar@w1r3.net"

class UvrError(Exception):
    pass
    
    
class UvrWait(UvrError):
    def __init__(self, message, timeout):
        super(UvrWait, self).__init__(message)
        self.timeout = timeout
        
        
class UvrResponseError(UvrError):
    def __init__(self, message, data):
        super(UvrResponseError, self).__init__(message)
        self.data = data
    def __str__(self):
        bytes = struct.unpack(len(self.data)*"B", self.data)
        bytesString = ' '.join([ "%02X" % x for x in bytes])
        return "%s (size: %d data: [%s])" % (str(self.message), len(bytes), bytesString)
        
class UvrChecksumError(UvrResponseError):
    pass

class UvrModeError(UvrError):
    pass
