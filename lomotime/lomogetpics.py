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
logo_imgurl = lomoconf.logo_url()

logo_done = False
bg_done = False
qr_done = False
ad_done = False

def get_pics():
    download_ok = True

    global logo_done
    global bg_done
    global qr_done
    global ad_done

    # get logo picture
    if not logo_done:
      logo_cmd = "~/client/lomogetlogo.sh " + logo_imgurl
      print logo_cmd
      logo_result = subprocess.check_output(logo_cmd, shell = True)
      print logo_result
      if logo_result == "0":
        logo_done = True
        print "logo downloaded"

    # get background picture
    req = requests.get(infurl, params = bgargs)
    if req.status_code == 200:
        # print req.text
        jpic = json.loads(req.text)
        back_pic = jpic["backPic"]

        if back_pic != "null" and (not bg_done):
          cmd = "~/client/lomodownload.sh " + base_imgurl + back_pic + " lomobg.jpg " + "/etc/lomotime/background.jpg"
          print "download cmd: " + cmd
          download_result = subprocess.check_output(cmd, shell = True)
          print download_result
          if download_result != "0":
            download_ok = False
          else:
            bg_done = True
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

        if dimen_pic != "null" and dimen_pic.endswith(".jpg") and (not qr_done):
          cmd = "~/client/lomodownload.sh " + dimen_pic + " lomoqrcode.jpg " + "/etc/lomotime/qrcode.jpg"
          print "download cmd: " + cmd
          download_result = subprocess.check_output(cmd, shell = True)
          print download_result
          if download_result != "0":
            download_ok = False
          else:
            qr_done = True

        if ad_pic != "null" and ad_pic.endswith(".jpg") and (not ad_done):
          cmd = "~/client/lomodownload.sh " + ad_pic + " lomoad.jpg " + "/etc/lomotime/ad.jpg"
          print "download cmd: " + cmd
          download_result = subprocess.check_output(cmd, shell = True)
          print download_result
          if download_result != "0":
            download_ok = False
          else:
            ad_done = True
    else:
        download_ok = False

    return download_ok

old_deleted = False
while True:
  if lomoutil.internet_on():
    # first, delete old images
    if not old_deleted:
      os.system("rm -f /etc/lomotime/background.jpg /etc/lomotime/qrcode.jpg /etc/lomotime/ad.jpg")
      old_deleted = True
      print "old bg deleted"
      
    try:
      result_ok = get_pics()
      if result_ok:
        break
    except Exception, e:
      # ignore 
      # print e
      pass
    time.sleep(interval)

