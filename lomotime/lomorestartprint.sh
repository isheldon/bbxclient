#!/bin/bash

printpid=`ps aux | grep lomoprint.py | grep -v grep | awk '{print $2}'`
kill -9 $printpid
~/client/lomoprint.py > /dev/null 2>&1 &

