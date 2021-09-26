#!/usr/bin/env python3
import sqlite3
import sys
import bgwChartGen

def usage():
    print("hourly.py <database> <output html>")

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
        c.execute("""select strftime('%Y-%m-%d %H', datetime(Timestamp, 'localtime')) hour, 
                        min(bw), max(bw), avg(bw) from (
                            select timestamp,
                                (deltasent * 8 / 1000000) / ((julianday(Timestamp) - julianday(lag(Timestamp, 1, 0) over ( order by Timestamp))) * 86400) bw 
                                from data) 
                        group by hour
                        order by hour desc limit 48""")

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
        f.write(bgwChartGen.MakeBWChart("Bandwidth Consumed (Mbps)", ("Min/Max BW (Mbps)", "Average BW (Mbps)"), rows))

if __name__ == "__main__":
    main(sys.argv[1:])
