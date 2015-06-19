#!/usr/bin/env python2

"""
This module contains the ReadRequest and ReadResponse classes which
are used to get a specific dataset from the bootloaders data flash.
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


class ReadRequest(Request):    
    def __init__(self, address, mode, frames):
        address = self.unfixAddress(address)
        data = struct.pack("BBBBB", READ_DATA, address[0], address[1], address[2], 1)
        self.data = self.addChecksum(data)
        self.mode = mode
        self.frames = frames
        if self.mode is CAN_MODE:
            self.length = 4+self.frames*CAN_DATA_LENGTH
        elif self.mode is DL_MODE:
            self.length = DL_DATA_LENGTH
        elif self.mode is DL2_MODE:
            self.length = DL2_DATA_LENGTH
        
    def unfixAddress(self, address):
        return [address & 0xFF, (address & 0x7F00)>>7, (address & 0xFF8000)>>15]
        
    def finished(self, data):
        if len(data) is self.length:
            return True
        else:
            return False
        
    def processResponse(self, data):
        if not self.validateChecksum(data):
            raise UvrChecksumError("Checksum error for ReadRequest", data)
        return ReadResponse(data, self.mode, self.frames)

            
class ReadResponse(object):
    def __init__(self, data, mode, frames):
        self.datasets = []
        parser = Parser()
        if mode is CAN_MODE:
            for i in range(frames):
                date = parser.parseDate(data[58+i*61: 64+i*61])
                dataset = parser.parseDataset(data[3+i*61: 58+i*61])
                date.update({"dataset": dataset})
                self.datasets.append(date)
        elif mode is DL_MODE:
            dataset = parser.parseDataset(data[0:55])
            date = parser.parseDate(data[55:61])
            date.update({"dataset": dataset})
            self.datasets.append(date)
        elif mode is DL2_MODE:
            dataset = parser.parseDataset(data[0:55])
            date = parser.parseDate(data[55:61])
            date.update({"dataset": dataset})
            self.datasets.append(date)
            dataset = parser.parseDataset(data[64:119])
            date = parser.parseDate(data[119:125])
            date.update({"dataset": dataset})
            self.datasets.append(date)