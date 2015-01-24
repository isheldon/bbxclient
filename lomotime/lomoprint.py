#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, subprocess, time, requests, json
import lomoconf, lomoutil
#import time #debug
import sys

reload(sys)
sys.setdefaultencoding( "utf-8" )

# read from config file
machine_id = lomoconf.machine_id()
base_imgurl = lomoconf.wximg_base_url()
wait_sec = lomoconf.print_interval()
pr_wait_sec = lomoconf.current_print_interval()

infurl = lomoconf.info_url()
list_args = {"method": "getBackPicList", "machineCode": machine_id}

printing_img = "/tmp/lomoprinting.jpg"
toprint_img = "/tmp/toprint.jpg"
voice_qrcode_img = "/tmp/weixinvoiceqrcode.jpg"
rm_printimg_cmd = "rm -f /tmp/lomoprinting.jpg"
cp_offline_cmd = "cp /etc/lomotime/default/offline.jpg " + printing_img

printed = []

while True:
  try:
    # print "begin loop: " + time.ctime() # debug

    # check network connection
    is_network_ok = lomoutil.internet_on()
    if not is_network_ok:
      os.system(cp_offline_cmd)

    else:
      images = []
      req = requests.get(infurl, params = list_args)
      if req.status_code == 200:
        # print req.text
        images = json.loads(req.text)

      print "images to be printed:"
      print images
      for image in images:
        row_id = image["id"] # row id, for later use after printing
        pic = image["picPath"] # picture path
        words = image["content"] # bottom side words of the photo
        is_win = image["isWin"] # lucky
        if words == "null":
          words = None
        pic_size = image["picSize"] # 1-small 2-big
        if pic_size == None or "1" == pic_size or "null" == pic_size:
          big_or_small = "S"
        else:
          big_or_small = "B"
        card_type = image["cardType"] # 9-voice
        if "9" == card_type:
          words = "扫一扫, 听声音"
          voice_qrcode_todownload = "http://122.225.105.51/weixinvoice/" + image["voiceQrcodeImg"]
          # download voice qrcode image to /tmp/weixinvoiceqrcode.jpg
          download_wxvoice_cmd = "~/client/lomodownload.sh " + voice_qrcode_todownload + " tmpwxvoiceqrcode.jpg " + voice_qrcode_img
          print download_wxvoice_cmd
          download_wxvoice_result = subprocess.check_output(download_wxvoice_cmd, shell = True)
          print "result: " +  download_wxvoice_result
          if download_wxvoice_result != "0":
            # download failed, go to next picture
            continue


        if pic is not None: 
          if pic in printed: # if already printed, skip it
            continue
          # check internet connection before download
          if not lomoutil.internet_on():
            break;
          # download picture to /tmp/toprint.jpg
          download_cmd = "~/client/lomodownload.sh " + base_imgurl + pic + " tmptoprint.jpg " + toprint_img
          print download_cmd
          download_result = subprocess.check_output(download_cmd, shell = True)
          print "result: " +  download_result
          if download_result != "0":
            # download failed, go to next picture
            continue

          #print "to run lomoprint.sh: " + time.ctime() # debug
          print_cmd = "~/client/lomoprint.sh " + big_or_small + " " + toprint_img + " " + is_win
          if words is not None: 
            print_cmd = print_cmd + " '" + words + "'"
          if "9" == card_type:
            print_cmd = print_cmd + " " + voice_qrcode_img
          print print_cmd # debug
          print_result = subprocess.check_output(print_cmd, shell = True)
          print "print result: " + print_result # debug

          #print "print finished: " + time.ctime() # debug

          if print_result == "0":
            # successfully printed, mark image printed, but check network first
            if lomoutil.internet_on():
              update_args = {"method": "getBackWeiXinId", "weiXinId": row_id}
              req = requests.get(infurl, params = update_args)
              if req.status_code != 200:
                printed.append(pic)
            else:
              printed.append(pic)

            #print "db updated: " + time.ctime() # debug
          else:
            # cancel this time of printing
            time.sleep(600) # wait 10 minutes for error process
            break
          # time.sleep(pr_wait_sec) #uncessary
      os.system(rm_printimg_cmd)
  except Exception, e:
    print e # debug
    os.system(rm_printimg_cmd)
  time.sleep(wait_sec)
# end wihle

