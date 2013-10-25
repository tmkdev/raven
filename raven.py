#!/usr/bin/python
import serial
import re
import time
from threading import Thread
import xml.etree.ElementTree as ET
import meter

def defaultHandler(thisMessage, type, meter):
    #print "%s: %s" % (type, str(thisMessage) )
    pass

class Raven:
    """
    Raven Utility meter class
    """
    readenable = True
    meters = {}

    def __init__(self,port):
        try:
            self._serial = serial.Serial(port, 115200)
        except:
            raise

        self.messagehandlers = []

    def dumpMessage(self, xml):
        """
        Extracts message from raw XML and sends to meter via update meter.
        @rtype : None
        """
        try:
            tree = ET.fromstring(xml)
            rawMessage = {'Type': tree.tag}
            for child in tree:
                try:
                    rawMessage[child.tag] = int(child.text, 16)
                except:
                    rawMessage[child.tag] = child.text

        except:
            rawMessage = {'Type': 'Invalid'}

        self.updateMeter(rawMessage)

    def updateMeter(self, rawmessage):
        """
        Handles attaching and logging message to meter. A list of messages are maintained by the meter.
        @rtype : None
        """
        try:
            if rawmessage['MeterMacId'] not in self.meters:
                self.meters[rawmessage['MeterMacId']] = meter.Meter(rawmessage['MeterMacId'])

        except:
            print "Message does not contain a MeterMacId"
            thismessage = {'Error': 'No Meter ID'}
            type = 'Invalid'

        if rawmessage['Type'] == 'InstantaneousDemand':
            type = 'InstantaneousDemand'
            thismessage = meter.InstantaneousDemand(rawmessage)
            self.meters[rawmessage['MeterMacId']].InstantaneousDemand.append(thismessage)

        elif rawmessage['Type'] == 'CurrentSummationDelivered':
            type = 'CurrentSummationDelivered'
            thismessage = meter.CurrentSummationDelivered(rawmessage)
            self.meters[rawmessage['MeterMacId']].CurrentSummationsDelivered.append(thismessage)
        else:
            type = 'UnknownMessage'
            thismessage = rawmessage

        if thismessage:
            for handler in self.messagehandlers:
                handler(thismessage, type, self.meters[rawmessage['MeterMacId']])


    def readMessage(self):
        """
        Threaded handler for serial to xml. Sends xml to dumpMessage for decoding
        @rtype : None
        """
        endtag = re.compile("</[A-Z]")
        xml = ""
        while self.readenable:
            line = self._serial.readline()
            xml += line
            if endtag.match(line):
                self.dumpMessage(xml)
                xml = ""

        self._serial.close()

    def start(self):
        """
        Starts serial port thread listener
        """
        t = Thread(target=self.readMessage)
        try:
            t.start()
            while True: time.sleep(10)
        except (KeyboardInterrupt, SystemExit):
            self.readenable = False

    def getMeterInfo(self):
        """
        Example command writer..
        """
        cmd = """<Command>
    <Name>get_meter_list</Name>
</Command>"""
        self._serial.write(cmd)

if __name__ == "__main__":
    myRaven = Raven('/dev/ttyUSB0')
    myRaven.messagehandlers.append(defaultHandler)
    myRaven.getMeterInfo()
    myRaven.start()


