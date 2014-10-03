#!/usr/bin/env python

import requests, json, os, time
import lomoconf, lomoutil

# read from config file
machine_id = lomoconf.machine_id()
imgurl = lomoconf.leftimg_base_url()

while True:

# download left side images when internect is connected
  if lomoutil.internet_on():
    # first, delete old images
    os.system("rm -f /etc/lomotime/leftmain.jpg*")
    os.system("rm -f /etc/lomotime/left*.jpg")

    # download the main left images
    for i in ["1", "2", "3", "4", "5"]:
      main_img_url = imgurl + "top_" + machine_id + "_" + i + ".jpg"
      # print "main, to download: " + main_img_url
      req = requests.get(main_img_url)
      if req.status_code == 200:
        download_cmd = "wget " + main_img_url + " -q -O /etc/lomotime/leftmain.jpg" + i
        print download_cmd
        os.system(download_cmd)

    # download the left small images
    for i in ["1", "2", "3"]:
      small_img_url = imgurl + "bottom_" + machine_id + "_" + i + ".jpg"
      # print "main, to download: " + main_img_url
      req = requests.get(small_img_url)
      if req.status_code == 200:
        download_cmd = "wget " + small_img_url + " -q -O /etc/lomotime/left" + i + ".jpg"
        print download_cmd
        os.system(download_cmd)

    # exit loop
    break

  time.sleep(10)

