#!/usr/bin/env python2

"""
This module contains the Socket class which contains the logic
needed for the socket communication with the bootloader.
"""

import logging
import socket

__author__ = "Bertram Winter, Dominic Miglar"
__copyright__ = "Copyright 2015"
__license__ = "GPL"
__maintainer__ = "Dominic Miglar"
__email__ = "dominic.miglar@w1r3.net"

logger = logging.getLogger(__name__)

def byte_to_hex(byte):
        hex = ''.join(["%02X " % ord(x) for x in byte]).strip()
        return '0x%s' % hex

class UvrSocket(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self):
        if self.sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        # DEBUG
        self.sock.settimeout(15.0)
        
    def close(self):
        self.sock.close()
        self.sock = None

    def request(self, request):
        msg = request.data
        totalsent = 0
        while totalsent < len(msg):
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent
        logger.debug("Request %s sent successfully" % byte_to_hex(msg))
        data = ''
        while not request.finished(data):
            bufsize = min(request.length - len(data), 2048)
            logger.debug("try to receieve %d byte(s) from socket.." % bufsize)
            chunk = self.sock.recv(bufsize)
            if chunk == '':
                raise RuntimeError("socket connection broken")
            data += chunk
            logger.debug("Received %d byte(s) from socket" % len(chunk))
        logger.debug("Total data received from socket: %d Byte(s)" % len(data))
        return request.processResponse(data)

