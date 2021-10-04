#!/bin/bash
./hourly.py bgw320.db /var/www/html/bgw320/hourly.html >& /dev/null
./bwhourly.py bgw320.db /var/www/html/bgw320/bw.html >& /dev/null
./dailydata.py bgw320.db /var/www/html/bgw320/daily.html >& /dev/null
