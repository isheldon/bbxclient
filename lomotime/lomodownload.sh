#!/bin/bash

download_url=$1
filename=$2
output_file=$3

wget --quiet --timeout=5 --tries=1 --output-document=/tmp/${filename} ${download_url} >/dev/null 2>&1

if [ "$?" == "0" ]; then
  mv -f /tmp/${filename} ${output_file}
  echo -n "0"
else
  rm -f /tmp/${filename}
  echo -n "1"
fi
