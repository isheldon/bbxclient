#!/bin/bash

printpid=`ps aux | grep lomoprint.pyc | grep -v grep | awk '{print $2}'`
kill -9 $printpid
python ~/client/lomoprint.pyc > /dev/null 2>&1 &

