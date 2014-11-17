#!/bin/bash

url=$1
wget --quiet --timeout=5 --tries=1 --output-document=/tmp/lomologo.jpg ${url} >/dev/null 2>&1

if [ "$?" == "0" ]; then
  mv -f /tmp/lomologo.jpg /etc/lomotime/logo.jpg
  echo -n "0"
else
  rm -f /etc/lomotime/logo.jpg
  rm -f /tmp/lomologo.jpg
  echo -n "1"
fi
