#!/usr/bin/env python

import requests, json, os, time
import lomoconf

# read from config file
machine_id = lomoconf.machine_id()
base_imgurl = lomoconf.img_base_url()
infurl = lomoconf.info_url()
args = {"method": "getBackGroundPic", "machineCode": machine_id}


def get_pics():
    req = requests.get(infurl, params = args)
    if req.status_code == 200:
        #print req.text
        jpic = json.loads(req.text)
        dimen_pic = jpic["dimenPic"]
        back_pic = jpic["backPic"]

        if dimen_pic != "null":
	    cmd = "sudo wget " + base_imgurl + dimen_pic + " -q -O /etc/lomotime/qrcode.jpg"
            os.system(cmd)
        if back_pic != "null":
	    cmd = "sudo wget " + base_imgurl + back_pic + " -q -O /etc/lomotime/background.jpg"
            os.system(cmd)

while True:
    try:
      get_pics()
    except Exception, e:
      # ignore 
      print ""
    time.sleep(60)

