#!/usr/bin/env python3
import configparser
import re
from datetime import datetime
import sqlite3
import sys, getopt

def usage():
    print("fetch.py [-c <configFile>]")
    print("   configFile - Defalts to rvwhisper.ini")

def fetchPage(url):
    # Fetch the given URL and return it as a string
    # Basically put here as a function for easy automatic cleanup
    import requests
    httpSession = requests.Session()
    r = httpSession.get(url)
    r.raise_for_status()
    return r.text


def main(argv):
    configFile = 'bgw320.ini'

    try:
        opts, args = getopt.getopt(argv, "c", ["config="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-c", "--config"):
            configFile = arg
         
    print("Reading %s" % configFile)
    config = configparser.ConfigParser()
    config.read(configFile)

    ipAddr = config.get('MAIN', 'ip', fallback = '192.168.1.254')

    pageContent = fetchPage("http://%s/cgi-bin/lanstatistics.ha" % ipAddr)

    p = re.compile('<table class="table100" cellpadding="1" summary="LAN Ethernet Statistics Table">(.+?)</table>', re.DOTALL)
    tblContents = p.search(pageContent).group(1)
    p = re.compile('Transmit Speed</td>(.+?)</tr>', re.DOTALL)
    speedBlock = p.search(tblContents).group(1)
    p = re.compile('Transmit Bytes</td>(.+?)</tr>', re.DOTALL)
    tranBlock = p.search(tblContents).group(1)
    p = re.compile('Receive Bytes</td>(.+?)</tr>', re.DOTALL)
    recvBlock = p.search(tblContents).group(1)

    # Each of these has 4 results, separated by physical port on the modem
    # I don't care about the individuals, so just get the numbers and sum them up
    p = re.compile('<td class="col2">(\d+)</td>', re.MULTILINE)
    speedBytes = sum(map(lambda x : int(x), p.findall(speedBlock)))
    print("Speed:  %s" % speedBytes)
    tranBytes = sum(map(lambda x : int(x), p.findall(tranBlock)))
    print("Transmit Bytes:  %s" % tranBytes)
    recvBytes = sum(map(lambda x : int(x), p.findall(recvBlock)))
    print("Receive Bytes:  %s" % recvBytes)

    # At this point both 'tranBytes' and 'recvBytes' should be a 4-element list containing the 
    # number of bytes transmitted/received ...

    # Now open/init the database.
    # Normally you would wrap this in a try/except block to catch any error..
    # But honestly, if we have an error here then the script should just exit with the error ...
    db = sqlite3.connect("bgw320.db")

    # Make sure the table we need exists.
    c = db.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS data (
                    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP PRIMARY KEY,
                    speed integer,
                    totalsent integer,
                    deltasent integer,
                    totalrecv integer,
                    deltarecv integer);""")

    # Now we need to calculate the Delta bytes sent/recv from the most recent total
    # There are 3 failure cases to handle
    #  1: There is no previous record.. This is the initialization state for a fresh DB
    #     In this we'll write the current Totals, and put in 0's for the delta
    #     This will avoid giant spikes when we start trying to calculate daily or hourly numbers 
    #  2: The previous record's total is more than the current total.. This is the "modem rebooted" state
    #     In this state, we'll use the Total _as_ the delta, since it should be pretty small
    #     Yes, our results won't be 100% Accurate but we can't recover those "missing" byte numbers
    #  3: This looks just like #2, except it's due to Integer overflow.
    #     Whenever the bytes transferred rolls over 2^32 (4gig), it resets to 0.  We _can_ recover
    #     This number by acknowledging the rollover, but detecting it via #2 above is hard.
    
    # So first, retrieve teh most recent record.

    c.execute("""select totalsent, totalrecv from data order by Timestamp desc limit 1""")
    previousTotals = c.fetchall()

    if(len(previousTotals) == 0):
        # This is the initialization state, nothing here to write.
        tranDelta = 0
        recvDelta = 0
    else:
        (ptranBytes, precvBytes) = map(lambda x: int(x), previousTotals[0])
 
        if (ptranBytes > tranBytes):
            # This is the case where the modem reset our numbers
            # This could be due to a reboot, or an overflow.. The numbers overflow at 2^32 (4 gig)
            if (ptranBytes > 3500000000):  # Honestly not sure if this is the best way to detect this
                tranDelta = tranBytes + (2**32 - ptranBytes)
            else:
                tranDelta = tranBytes
        else:
            # This is our "normal" case.. CAlculcate the diff's
            tranDelta = tranBytes - ptranBytes

        # You may be asked "Why do this twice?"
        # Seems teh modem automatically resets the numbers at the 4gig mark , but manages
        # each of them separately...  So in that case, Trans would reset but recv wouldn't.
        if (precvBytes > recvBytes):
            if (precvBytes > 3500000000):
                recvDelta = recvBytes + (2**32 - precvBytes)
            else :
                recvDelta = recvBytes
        else:
            recvDelta = recvBytes - precvBytes

    # Now insert into the DB
    c.execute("INSERT INTO data(speed, totalsent, deltasent, totalrecv, deltarecv) values(?,?,?,?,?)",
                (speedBytes, tranBytes, tranDelta, recvBytes, recvDelta))

    # And we're done!
    db.commit()
    db.close()

if __name__ == "__main__":
    main(sys.argv[1:])

