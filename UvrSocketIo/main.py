#!/usr/bin/env python2

"""
User-Friendly CLI tool to communicate with the bootlaoder
"""

import logging
import sys
from logging.config import dictConfig
from uvrconnection import UvrConnection
from uvrerrors import *

__author__ = "Dominic Miglar"
__copyright__ = "Copyright 2015"
__license__ = "GPL"
__maintainer__ = "Dominic Miglar"
__email__ = "dominic.miglar@w1r3.net"

LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'root': {
                'handlers': ['console',],
                'level': 'DEBUG',
            },
        'formatters': {
            'simple': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(lineno)s - %(funcName)s - %(message)s',
                 'datefmt': '%Y %b %d, %H:%M:%S',
                },
            },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
            #'main_file': {
            #    'level': 'DEBUG',
            #    'class': 'logging.handlers.RotatingFileHandler',
            #    'filename': 'main_file.log',
            #    'formatter': 'simple',
            #    'maxBytes': 1024*1024,
            #},
        },
    }

def print_usage():
    print('Usage: %s [getfirmware|getlatest|getdata|resetdata]' % sys.argv[0])

def print_dataset_raw(dataset):
    print(dataset[0])
    print(dataset[0].analog)
    print(dataset[0].digital)
    print(dataset[0].energy)

def print_dataset(dataset):
    print("Analog Values:")
    print("----------------------------")
    for i in range(0, len(dataset.analog)):
        unit = dataset.analog[i]['unit']
        if unit == 'C':
            unit = u'\N{DEGREE SIGN}%s' % unit
        print("Analog %d:\t %.1f %s" % (i+1, dataset.analog[i]['value'], unit))
    print("\nDigital Values:")
    print("----------------------------")
    for i in range(0, len(dataset.digital)):
        print("Digital %d:\t %d %s %s" % (
            i+1, dataset.digital[i]['value'], dataset.digital[i]['unit'], dataset.digital[i].get('speed', '')))
    print("\nEnergy Values:")
    print("----------------------------")
    for i in range(0, len(dataset.energy)):
        print("Energy %d:\t Active: %d, Energy: %f kWh, Power: %f kW" % (i+1, dataset.energy[i]['active'], dataset.energy[i]['energy'], dataset.energy[i]['power'],))

def datetime_to_string(date):
    return date.strftime("%Y-%m-%d %H:%M:%S")

def get_latest():
    try:
        uvr = UvrConnection('172.24.255.60', 40000)
        latest = uvr.getLatest()
        for dataset in latest:
            print_dataset(dataset)
    except UvrError as e:
        print(e)

def get_data():
    try:
        uvr = UvrConnection('172.24.255.60', 40000)
        data = uvr.getData()
        #for datadict in data:
        #    print("\nDate: %s" % str(datadict[0]['date']))
        #    print_dataset(datadict[0]['dataset'])
        for datalist in data:
            for datadict in datalist:
                print('\nDate and Time: %s' % datetime_to_string(datadict['date']))
                print_dataset(datadict['dataset'])
    except UvrError as e:
        print(e)

def reset_data():
    try:
        uvr = UvrConnection('172.24.255.60', 40000)
        uvr.resetData()
        print('Data reset!')
    except UvrError as e:
        print(e)

def get_firmware():
    try:
        uvr = UvrConnection('172.24.255.60', 40000)
        firmware = uvr.getFirmware()
        print(firmware)
    except UvrError as e:
        print(e)

def main():
    if(len(sys.argv) < 2):
        print_usage()
        sys.exit(-1)
    elif(sys.argv[1] == 'getfirmware'):
        get_firmware()
    elif(sys.argv[1] == 'getlatest'):
        get_latest()
    elif(sys.argv[1] == 'getdata'):
        get_data()
    elif(sys.argv[1] == 'resetdata'):
        reset_data()
    else:
        print_usage()
        sys.exit(-1)


if __name__ == "__main__":
    dictConfig(LOGGING_CONFIG)
    main()
