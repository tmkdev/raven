#!/usr/bin/python
import sqlite3
import raven
import os

def defaultHandler(thismessage, type, meter):
    if hasattr(meter, 'meterId'):

        conn = sqlite3.connect('db/meters.db')
        c = conn.cursor()

        if type == 'InstantaneousDemand':
            c.execute('insert into instantaneousdemand ( metermacid, date, demand ) values ( ?, ? , ?)',
                      ( meter.meterId, thismessage.Timestamp, thismessage.Demand))

        if type == 'CurrentSummationDelivered':
            c.execute('insert into summationdelivered ( metermacid, date, summationdelivered ) values ( ?, ?, ?)',
                      ( meter.meterId, thismessage.Timestamp, thismessage.SummationDelivered))

        conn.commit()
        conn.close()


def createDb():
    if not os.path.exists('./db'):
        os.makedirs('./db')

    conn = sqlite3.connect('db/meters.db')
    c = conn.cursor()

    c.execute("""create table if not exists meters ( metermacid int, metername text, primary key (metermacid) )""")
    c.execute(
        """create table if not exists instantaneousdemand ( metermacid int, date int, demand numeric, tstamp CURRENT_TIME DEFAULT CURRENT_TIMESTAMP )""")
    c.execute(
        """create table if not exists summationdelivered ( metermacid int, date int, summationdelivered numeric, tstamp CURRENT_TIME DEFAULT CURRENT_TIMESTAMP)""")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    createDb()
    myRaven = raven.Raven('/dev/ttyUSB0')
    myRaven.messagehandlers.append(defaultHandler)
    myRaven.getMeterInfo()
    myRaven.start()
