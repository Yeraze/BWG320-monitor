#!/usr/bin/env python3
import sqlite3
import sys
import bgwChartGen


def usage():
    print("dailydata.py <database> <output html>")

def main(argv):
    if (len(argv) != 2):
        usage()
        sys.exit(2)

    database = argv[0]
    outfile = argv[1]
    print("Reading from %s" % database)
    print("Generating %s" % outfile)
    # Retrieve the necessary data
    try:
        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute("select strftime('%Y-%m-%d', datetime(Timestamp, 'localtime')) day, sum(deltarecv) / 1000000, sum(deltasent) / 1000000 from data group by day order by day desc limit 30")
        rows = c.fetchall()
        conn.close()

    except sqlite3.Error as e:
        print(e)
        sys.exit(2)

    # Reverse the data since it's 'order by hour desc'
    rows.reverse()

    # Now we have a nice trivial chart to generate... 
    # 'rows' should contain a list of simple 3-element tuples (Timestamp, Bytes Received, Bytes Sent)
    # Now, I plan to generate a few of these.. Hourly and Daily bandwidth.. maybe even Monthly.

    # Now, the astute among you may notice that I've got the UPload/Download titles backwards.
    # This is because the data collected is backwards.. Kinda.
    #  "Bytes Sent" is "Sent to the LAN port", not sent Upstream.  So that's actually data Downloaded from the network
    with open(outfile, 'w') as f:
        f.write(bgwChartGen.MakeChart("dailydata", "Daily Data Consumption", ("MBytes Upload", "MBytes Download"), rows))

if __name__ == "__main__":
    main(sys.argv[1:])
