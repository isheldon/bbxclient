#!/usr/bin/env python

import requests, json, os, time

idfile = open('/etc/bobox/device_id', "r")
try:
    device_id = idfile.read().rstrip('\n')
finally:
    idfile.close()

infurl = "http://www.lomotime.cn/admin/mims/reg.do"
args = {"method": "getMachinePic", "machineCode": device_id}

base_imgurl = "http://122.225.105.20:8080/uploadImg/img/"


def get_pics():
    req = requests.get(infurl, params = args)
    if req.status_code == 200:
        jpic = json.loads(req.text)
        dimen_pic = jpic["dimenPic"]
        logo_pics = jpic["picUrls"]

        if dimen_pic != "null":
	    cmd = "sudo wget " + base_imgurl + dimen_pic + " -q -O /etc/bobox/qrcode.jpg"
            os.system(cmd)
        if len(logo_pics) > 0:
            os.system("sudo rm -f /etc/bobox/logos/*.jpg")
	    for logo in logo_pics:
	        cmd = "sudo wget " + base_imgurl + logo + " -q -O /etc/bobox/logos/" + logo
                os.system(cmd)

while True:
    get_pics()
    time.sleep(60)

