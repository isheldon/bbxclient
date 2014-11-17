#!/usr/bin/env python

import requests, json, os, time, subprocess, urllib2
import lomoconf, lomoutil

# read from config file
machine_id = lomoconf.machine_id()
imgurl = lomoconf.leftimg_base_url()
old_deleted = False

while True:

# download left side images when internect is connected
  if lomoutil.internet_on():
    # first, delete old images
    if not old_deleted:
      os.system("rm -f /etc/lomotime/leftmain.jpg*")
      os.system("rm -f /etc/lomotime/left*.jpg")
      old_deleted = True
      print "old left images deleted" #debug

    # download the main left images
    download_ok = True
    for i in ["1", "2", "3", "4", "5"]:
      main_img_url = imgurl + "top_" + machine_id + "_" + i + ".jpg"

      try:
        urllib2.urlopen(urllib2.Request(main_img_url))
        img_url_ok = True
      except:
        img_url_ok = False
        
      if img_url_ok:
        # download_cmd = "wget " + main_img_url + " -q -O /etc/lomotime/leftmain.jpg" + i
        download_cmd = "~/client/lomodownload.sh " + main_img_url + " leftmain.jpg " + "/etc/lomotime/leftmain.jpg" + i
        print download_cmd + time.ctime() #debug
        download_result = subprocess.check_output(download_cmd, shell = True)
        print download_result + time.ctime() #debug
        if download_result != "0":
          download_ok = False

    # download the left small images
    for i in ["1", "2", "3"]:
      small_img_url = imgurl + "bottom_" + machine_id + "_" + i + ".jpg"
      print "small, to download: " + small_img_url

      try:
        urllib2.urlopen(urllib2.Request(small_img_url))
        img_url_ok = True
      except:
        img_url_ok = False

      if img_url_ok:
        # download_cmd = "wget " + small_img_url + " -q -O /etc/lomotime/left" + i + ".jpg"
        download_cmd = "~/client/lomodownload.sh " + small_img_url + " leftsmall.jpg " + "/etc/lomotime/left" + i + ".jpg"
        print download_cmd + time.ctime() #debug
        download_result = subprocess.check_output(download_cmd, shell = True)
        print download_result + time.ctime() #debug
        if download_result != "0":
          download_ok = False

    # exit loop if all downloaded
    if download_ok:
      break

  time.sleep(10)

