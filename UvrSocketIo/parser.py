#!/usr/bin/env python2

"""
This module contains the Parser class which is able to parse the binary
formatted output from the bootloader to python data structures.
"""

import logging
import struct
from datetime import datetime
from uvrerrors import UvrError

__author__ = "Bertram Winter, Dominic Miglar"
__copyright__ = "Copyright 2015"
__license__ = "GPL"
__maintainer__ = "Dominic Miglar"
__email__ = "dominic.miglar@w1r3.net"

SIGN_BIT = 0x8000;
POSITIVE_VALUE_MASK = 0x00000FFF;
SPEED_ACTIVE = 0x80;
SPEED_MASK = 0x1F;
TYPE_MASK = 0x7000;
TYPE_NONE = 0x0000;
TYPE_DIGITAL = 0x1000;
TYPE_TEMP = 0x2000;
TYPE_VOLUME = 0x3000;
TYPE_RADIATION = 0x4000;
TYPE_RAS = 0x7000;
RAS_POSITIVE_MASK = 0x000001FF;
INT32_MASK = 0xFFFFFFFF;
INT32_SIGN = 0x80000000;

logger = logging.getLogger(__name__)

class Parser(object):
    def parseDate(self, data):
        logger.debug("Entered Parser.parseDate function")
        second, minute, hour, day, month, year = struct.unpack("<BBBBBB", data)
        logger.debug("Second: %d, Minute: %d, Hour: %d, Day: %d, Month: %d, Year: %d" % (second, minute, hour, day, month, year))
        ## IF INVALID VALUES ARE SAVED IN BL-NET
        if(second == minute == hour == day == month == year == 255):
            raise UvrError('Got malformed date to parse')
            #return {"date": None}
        if(month == 0):
            raise UvrError('Got malformed date to parse')
            #return {"date": None}
        date = datetime(2000+year, month, day, hour, minute, second)
        return {"date": date}
    
    def parseDataset(self, data):
        logger.debug("Entered Parser.parseDataset function")
        raw = struct.unpack("<HHHHHHHHHHHHHHHHHBBBBBIHHIHH", data)
        dataset = Dataset()
        for i in range(16):
            dataset.analog.append(self.__convAnalog(raw[0+i]))
            
        #for i in range(16): # 16 Bits, but only 13 in use (other 3 are x - don't care!)
        for i in range(13):
            dataset.digital.append(self.__convDigital(raw[16]>>i))

        for i in range(4):
            mapping = [0,1,5,6] #A1, A2, A6, A7 (n-1)
            value = self.__convSpeed(raw[17+i])
            if value:
                logger.debug("SPEED VALUE %d: %d" % (i, value['speed']))
            if value is not None:
                dataset.digital[mapping[i]].update(value)
                
        for i in range(2):
            dataset.energy.append(self.__convEnergy(raw[21]>>i, raw[22+i*3], raw[23+i*3:25+i*3]))
            
        return dataset
        
    def __convAnalog(self, value):
        result = value & POSITIVE_VALUE_MASK

        if value & SIGN_BIT:
            result = -((result ^ POSITIVE_VALUE_MASK) + 1)

        valueType = value & TYPE_MASK
        if valueType == TYPE_TEMP:
            return {"value": result/float(10), "unit": "C"}
        elif valueType == TYPE_VOLUME:
            return {"value": result*4, "unit": "l/min"}
        elif valueType == TYPE_DIGITAL:
            if value & SIGN_BIT:
                return {"value": 1, "unit": "digital"}
            else:
                return {"value": 0, "unit": "digital"}
        elif valueType == TYPE_RAS:
            result = value & RAS_POSITIVE_MASK
            if value & SIGN_BIT:
                result = -((result ^ RAS_POSITIVE_MASK) + 1)
            return {"value": result/float(10), "unit": "C"}
        elif valueType == TYPE_RADIATION:
            return {"value": result, "unit": "W/m2"}
        else:
            return {"value": result, "unit": "analog"}
     
    def __convDigital(self, value):
        if value & 0x0001:
            return {"value": 1, "unit": "digital"}
        else:
            return {"value": 0, "unit": "digital"}


    def __convSpeed(self, value):
        if value & SPEED_ACTIVE:
            return None
        else:
            speed = value & SPEED_MASK
            return {"speed": speed}
        
    def __convEnergy(self, active, power, energy):
        if power & INT32_SIGN:
            power = -((power ^ INT32_MASK) + 1)
        # energy[1] -> MWh -> [in 1 MWh]
        # energy[0] -> kWh -> [in 1/10 kWh]
        # energy_value = MWh * 1000 + kWh / 10
        kwh = energy[0]
        mwh = energy[1]
        energy_value = mwh*1000+float(kwh)/10
        power_value = power/float(2560)
        return {"active": active & 0x01, "power": power_value, "energy": energy_value}


class Dataset(object):
    def __init__(self):
        self.analog = []
        self.digital = []
        self.energy = []
