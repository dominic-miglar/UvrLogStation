#!/usr/bin/env python2

"""
This module contains various serializers which are used to represent the
data from the UvrSocketIo library as JSON-Formatted strings.
"""

import json

__author__ = "Dominic Miglar"
__copyright__ = "Copyright 2015"
__license__ = "GPL"
__maintainer__ = "Dominic Miglar"
__email__ = "dominic.miglar@w1r3.net"


class UvrSerializer(object):
    def __init__(self, data):
        self.data = data

    def prepare_data(self):
        raise NotImplementedError()

    def serialize(self):
        prepared_data = self.prepare_data()
        return json.dumps(prepared_data)


class UvrDataSerializer(UvrSerializer):

    def datetime_to_string(self, date):
        return date.strftime("%Y-%m-%d %H:%M:%S")

    def prepare_data(self):
        serializable_data = []
        for datalist in self.data:
            datestring = None
            dataset = None
            for datadict in datalist:
                if datestring is None:
                    datestring = self.datetime_to_string(datadict['date'])
                if dataset is None:
                    dataset = datadict['dataset']
                else:
                    dataset.analog.extend(datadict['dataset'].analog)
                    dataset.digital.extend(datadict['dataset'].digital)
                    dataset.energy.extend(datadict['dataset'].energy)
            analog_list = []
            for i in range(len(dataset.analog)):
                name = 'Analog%d' % (i+1)
                analog_list.append({'name': name, 'value': dataset.analog[i]['value'], 'unit': dataset.analog[i]['unit']})
            digital_list = []
            for i in range(len(dataset.digital)):
                name = 'Digital%d' % (i+1)
                digitaldict = {'name': name, 'value': dataset.digital[i]['value'], 'unit': dataset.digital[i]['unit']}
                speed = dataset.digital[i].get('speed', None)
                if speed is not None:
                    digitaldict.update({'speed': speed})
                digital_list.append(digitaldict)
            energy_list = []
            for i in range(len(dataset.energy)):
                name = 'HeatMeter%d' % (i+1)
                energy_list.append({'name': name, 'power': dataset.energy[i]['power'], 'energy': dataset.energy[i]['energy']})
            serializable_data.append({'date': datestring, 'analog': analog_list, 'digital': digital_list, 'energy': energy_list})
        return serializable_data

class UvrLatestSerializer(UvrSerializer):
    pass

