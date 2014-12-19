#!/bin/bash

# handle upgrade package first
if [ -d ~/client.new ]
then
  mv ~/client ~/client.bak
  mv ~/client.new ~/client
fi

python /home/lomotime/client/lomogetcode.pyc > /dev/null 2>&1 &
python /home/lomotime/client/lomogetleftpics.pyc > /dev/null 2>&1 &
python /home/lomotime/client/lomogetpics.pyc > /dev/null 2>&1 &
python /home/lomotime/client/lomoprint.pyc > /dev/null 2>&1 &
python /home/lomotime/client/lomoclient.pyc > /dev/null 2>&1 &

