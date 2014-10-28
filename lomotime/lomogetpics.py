#!/usr/bin/env python

import requests, json, os, time
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
	    cmd = "sudo wget " + base_imgurl + back_pic + " -q -O /etc/lomotime/background.jpg"
            os.system(cmd)
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
	    cmd = "sudo wget " + dimen_pic + " -q -O /etc/lomotime/qrcode.jpg"
            os.system(cmd)
        if ad_pic != "null" and ad_pic.endswith(".jpg"):
	    cmd = "sudo wget " + ad_pic + " -q -O /etc/lomotime/ad.jpg"
            os.system(cmd)
    else:
        download_ok = False

    return download_ok

while True:
  if lomoutil.internet_on():
    try:
      result_ok = get_pics()
      if result_ok:
        break
    except Exception, e:
      # ignore 
      print ""
    time.sleep(interval)

