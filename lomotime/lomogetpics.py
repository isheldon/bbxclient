#!/usr/bin/env python

import requests, json, os, time, subprocess
import lomoconf, lomoutil

# read from config file
machine_id = lomoconf.machine_id()
base_imgurl = lomoconf.img_base_url()
infurl = lomoconf.info_url()
bgargs = {"method": "getBackGroundPic", "machineCode": machine_id}
adargs = {"method": "getAD", "machineCode": machine_id}
interval = lomoconf.qrcode_interval()

def get_pics():
    download_ok = True
    # get background picture
    req = requests.get(infurl, params = bgargs)
    if req.status_code == 200:
        # print req.text
        jpic = json.loads(req.text)
        back_pic = jpic["backPic"]

        if back_pic != "null":
          cmd = "~/client/lomodownload.sh " + base_imgurl + back_pic + " lomobg.jpg " + "/etc/lomotime/background.jpg"
          # print "download cmd: " + cmd
          download_result = subprocess.check_output(cmd, shell = True)
          # print download_result
          if download_result != "0":
            download_ok = False
    else:
        download_ok = False

    req = requests.get(infurl, params = adargs)
    if req.status_code == 200:
        # print req.text
        jpic = json.loads(req.text)
        dimen_pic = jpic["dimenCode"]
        ad_pic = jpic["photoPrinting"]
        # print dimen_pic
        # print ad_pic

        if dimen_pic != "null" and dimen_pic.endswith(".jpg"):
          cmd = "~/client/lomodownload.sh " + dimen_pic + " lomoqrcode.jpg " + "/etc/lomotime/qrcode.jpg"
          # print "download cmd: " + cmd
          download_result = subprocess.check_output(cmd, shell = True)
          # print download_result
          if download_result != "0":
            download_ok = False

        if ad_pic != "null" and ad_pic.endswith(".jpg"):
          cmd = "~/client/lomodownload.sh " + ad_pic + " lomoad.jpg " + "/etc/lomotime/ad.jpg"
          # print "download cmd: " + cmd
          download_result = subprocess.check_output(cmd, shell = True)
          # print download_result
          if download_result != "0":
            download_ok = False
    else:
        download_ok = False

    return download_ok

while True:
  if lomoutil.internet_on():
    # first, delete old images
    os.system("rm -f /etc/lomotime/background.jpg /etc/lomotime/qrcode.jpg /etc/lomotime/ad.jpg")
    try:
      result_ok = get_pics()
      if result_ok:
        break
    except Exception, e:
      # ignore 
      pass
    time.sleep(interval)

