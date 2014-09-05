#!/bin/bash

url=$1
#echo "logo: $url"
wget $url -q -O /etc/lomotime/logo.jpg
if [ "$?" != "0" ]; then
  rm -f /etc/lomotime/logo.jpg
fi

