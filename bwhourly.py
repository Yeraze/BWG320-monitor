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
        c.execute("""select strftime('%Y-%m-%d %H:00', datetime(Timestamp, 'localtime')) hour, 
                        min(bw1), max(bw1), avg(bw1),
                        min(bw2), max(bw2), avg(bw2)
                        from (
                            select timestamp,
                                (deltasent * 8 / 1000000) / ((julianday(Timestamp) - julianday(lag(Timestamp, 1, 0) over ( order by Timestamp))) * 86400) bw1,
                                (deltarecv * 8 / 1000000) / ((julianday(Timestamp) - julianday(lag(Timestamp, 1, 0) over ( order by Timestamp))) * 86400) bw2 
                                from data
                        ) 
                        group by hour
                        order by hour desc limit 24""")

        rows = c.fetchall()
        conn.close()

    except sqlite3.Error as e:
        print(e)
        sys.exit(2)

    # Reverse the data since it's 'order by hour desc'
    rows.reverse()

    # Now we have a nice trivial chart to generate... 
    # 'rows' should contain a list of simple 4-element tuples (Timestamp, Min bandwidth, Max bandwidth received, average bandwidth)
    # Now, I plan to generate a few of these.. Hourly and Daily bandwidth.. maybe even Monthly.

    # Send them to the function to render the 3 datapoints as a Bar from Min to Max, and a line through the Averages
    with open(outfile, 'w') as f:
        f.write(bgwChartGen.MakeBWChart("Bandwidth Consumed (Mbps)", ("Download Min/Max BW (Mbps)", "Download Average BW (Mbps)", "Upload Min/Max BW (Mbps)", "Upload Average BW (Mbps)"), rows))

if __name__ == "__main__":
    main(sys.argv[1:])
