#!/usr/bin/python
import datetime

_epoch2000 = 946684800


class Meter:
    InstantaneousDemand = []
    CurrentSummationsDelivered = []
    meterId = 0

    def __init__(self):
        pass

    def __init__(self, meterid):
        self.meterId = meterid

    def __str__(self):
        return "0x%x" % self.meterId


#{'DeviceMacId': 15624597891882945219L, 'Divisor': 1000, 'TimeStamp': 435556671, 'MeterMacId': 2112161838820854,
# 'Multiplier': 1, 'DigitsRight': 1, 'DigitsLeft': 6, 'SuppressLeadingZero': 'Y', 'SummationReceived': 0,
# 'SummationDelivered': 13284552, 'Type': 'CurrentSummationDelivered'}
class CurrentSummationDelivered:
    Timestamp = 0
    SummationDelivered = 0

    def __init__(self, rawmessage):
        try:
            self.Timestamp = rawmessage['TimeStamp'] + _epoch2000
            self.SummationDelivered = round(
                (float(rawmessage['SummationDelivered']) * rawmessage['Multiplier']) / rawmessage['Divisor'],
                rawmessage['DigitsRight'])
        except:
            print rawmessage

    def __str__(self):
        return "CurrentSummationDelivered,%s,%.1f" % (
        datetime.datetime.fromtimestamp(self.Timestamp), self.SummationDelivered )


class InstantaneousDemand:
    def __init__(self, rawMessage):
        self.Timestamp = rawMessage['TimeStamp'] + _epoch2000
        self.Demand = round((float(rawMessage['Demand']) * rawMessage['Multiplier']) / rawMessage['Divisor'],
                            rawMessage['DigitsRight'])

    def __str__(self):
        return "InstantDemand,%s,%.3f" % (datetime.datetime.fromtimestamp(self.Timestamp), self.Demand)



