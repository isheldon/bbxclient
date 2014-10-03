#!/bin/bash

orig_img=$1
words=$2

cd ~/client
# echo "image: $orig_img, words: $words"
# generate image for printing: /tmp/999.jpg; and image for display: /tmp/lomoprinting.jpg
if [ -z $words ]; then
  # no words
  if [ -f /etc/lomotime/ad.jpg ]; then
    java GenerateImage ${orig_img} "" /etc/lomotime/ad.jpg
  elif [ -f /etc/lomotime/logo.jpg ]; then
    java GenerateImage ${orig_img} "" /etc/lomotime/logo.jpg
  else
    java GenerateImage ${orig_img} ""
  fi
else
  # there's words
  if [ -f /etc/lomotime/logo.jpg ]; then
    java GenerateImage ${orig_img} "${words}" /etc/lomotime/logo.jpg
  else
    java GenerateImage ${orig_img} "${words}"
  fi
fi

# use commandline tool (lpr) to print image
lpr /tmp/999.jpg

# check print job queue,
# if job not finished within 30 seconds, something wrong
err=1
for i in 1 2 3 4
do
  sleep 10s
  # check job count, 0 means job finished
  job=`lpstat | wc -l`
  # echo "try ${i}, job=${job}"
  if [ $job -eq 0 ]; then
    # echo "job finished"
    err=0
    break
  fi
done

# echo "err: ${err}"
# if there is any error, cancel job
if [ $err -eq 1 ]; then
  cancel -a
  cp -f /etc/lomotime/default/printerr.jpg /tmp/lomoprinting.jpg
  echo -n "1"
  exit 0
else
  echo -n "0"
  exit 0
fi

