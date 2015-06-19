#!/usr/bin/env python2
# txlog.py 'transmit log'

"""
Reads the logged data out of the bootloader and sends it to
the backend server.
"""

import codecs
import os
import sys
from ConfigParser import SafeConfigParser
import logging
from logging.config import dictConfig
import socket
from uvrlogreader import UvrLogReader
from uvrlogsysclient import UvrLogSysClient, UvrLogSysError, UvrResponseError
from UvrSocketIo.uvrerrors import *

__author__ = "Dominic Miglar"
__copyright__ = "Copyright 2015"
__license__ = "GPL"
__maintainer__ = "Dominic Miglar"
__email__ = "dominic.miglar@w1r3.net"

CONFIGURATION_FILE_NAME = 'config.ini'


def generate_logging_config():
    log_level = parse_config_file()['logging']['log_level']
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'root': {
                'handlers': ['console',],
                'level': log_level,
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
    return logging_config


def configure_logger():
    dictConfig(generate_logging_config())


def parse_config_file():
    configuration_file = os.path.abspath(os.path.dirname(__file__))+'/'+CONFIGURATION_FILE_NAME
    parser = SafeConfigParser()
    with codecs.open(configuration_file, 'r', encoding='utf-8') as config_file:
        parser.readfp(config_file)
    uvr_ip = parser.get('UVR1611', 'ip_address')
    uvr_port = int(parser.get('UVR1611', 'tcp_port'))
    backend_url = parser.get('Backend', 'url')
    backend_username = parser.get('Backend', 'username')
    backend_password = parser.get('Backend', 'password')
    backend_controller_name = parser.get('Backend', 'controller_name')
    log_level = parser.get('Logging', 'log_level')
    return {'controller': {'ip': uvr_ip, 'port': uvr_port}, 'backend': {'url': backend_url,
        'ctrlname': backend_controller_name,'username': backend_username, 'password': backend_password},
        'logging': {'log_level': log_level}}

def main():
    logger = logging.getLogger(__name__)
    configuration = parse_config_file()

    try:
        uvrlogreader = UvrLogReader(configuration['controller']['ip'], configuration['controller']['port'])
        uvrlogsysclient = UvrLogSysClient(configuration['backend']['url'],
            configuration['backend']['ctrlname'])
        logger.info('Getting logged data from %s:%d' % (uvrlogreader.uvrhost, uvrlogreader.uvrport))
        logdata = uvrlogreader.getData()
        if logdata:
            logger.info('Successfully got logged data.')
        else:
            logger.info('No logging data available! Exiting..')
            sys.exit()
        logger.info('Sending logged data to backend host')
        if(uvrlogsysclient.postUvrData(logdata)):
            logger.info('Data sent to backend server successfully!')
            logger.info('Reset data log flash on BL-NET')
            uvrlogreader.resetData()
            logger.info('DONE!\n')
        else:
            logger.error('Sending logged data to backend host failed!')
    except socket.timeout as e:
        logger.error(e.message)
        sys.exit(e.message)
    except socket.error as e:
        logger.error(e.message)
        sys.exit(e.message)
    except UvrResponseError as e:
        logger.error(e.message)
        sys.exit(e.message)
    except UvrError as e:
        logger.error(e.message)
        sys.exit(e.message)
    except UvrLogSysError as e:
        logger.error(e.message)
        sys.exit(e.message)
    except Exception as e:
        logger.error(e.message)
        sys.exit(e.message)


if __name__ == '__main__':
    configure_logger()
    main()
