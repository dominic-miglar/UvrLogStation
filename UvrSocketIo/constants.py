#!/usr/bin/env python2

"""
This module contains various constants which are used for the communication
with the bootloader BL-NET and the UVR1611.
"""

__author__ = "Bertram Winter, Dominic Miglar"
__copyright__ = "Copyright 2015"
__license__ = "GPL"
__maintainer__ = "Dominic Miglar"
__email__ = "dominic.miglar@w1r3.net"


GET_LATEST = 0xAB
GET_HEADER = 0xAA
GET_MODE = 0x81
GET_FIRMWARE = 0x82
READ_DATA = 0xAC
END_READ = 0xAD
RESET_DATA = 0xAF

WAIT_TIME = 0xBA

CAN_MODE = 0xDC
DL_MODE = 0xA8
DL2_MODE = 0xD1

MAX_ADDRESS = 0x07FFFF

END_READ_LENGTH = 1
RESET_LENGTH = 1
CAN_HEADER_LENGTH = 21
DL_HEADER_LENGTH = 13
DL2_HEADER_LENGTH = 14
CAN_LATEST_LENGTH = 57
DL_LATEST_LENGTH = 57
DL2_LATEST_LENGTH = 113
CAN_DATA_LENGTH = 61
DL_DATA_LENGTH = 65
DL2_DATA_LENGTH = 126
WAIT_LENGTH = 3
MODE_LENGTH = 1
FIRMWARE_LENGTH = 1

