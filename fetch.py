#!/usr/bin/env python3
import configparser
import requests
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

    print(tblContents)


if __name__ == "__main__":
    main(sys.argv[1:])

