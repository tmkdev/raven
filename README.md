raven
=====
Rainforest automation raven implmentation in python


TMKDEV LLC
t_kolody@yahoo.ca

This is free software - as in beer. If you use this - you have been warned that it may have bugs and I am not
responsible for them. But send them to me and I'll fix them. Or donate code to the effort!

If you use this in a commercial application, I ask that you give me credit.



raven - handles communications with the raven USB device.
meter - meter class holds meter info and creates and attaches messages to the meter recieved from the raven class.
logging - logs data to a sqllite3 database. Use this to see how a message handleer is built and implementented.

Only 2 messages are implemented in this VERY early alpha release.

usage: python logger.py

It will create a db in ./db and log data to it. Control-c kills it.
Assumes your raven USB device is at /dev/ttyUSB0. If it's not - then, well, change it!