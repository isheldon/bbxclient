#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb, os, subprocess, time, requests
import lomoconf, lomoutil
# import time # debug

# read from config file
machine_id = lomoconf.machine_id()
base_imgurl = lomoconf.wximg_base_url()
logo_imgurl = lomoconf.logo_url()
db_host = lomoconf.db_host()
db_usr = lomoconf.db_usr()
db_pwd = lomoconf.db_pwd()
db_name = lomoconf.db_name()
db_port = lomoconf.db_port()
wait_sec = lomoconf.print_interval()
pr_wait_sec = lomoconf.current_print_interval()
checkUrl = lomoconf.check_url()

printing_img = "/tmp/lomoprinting.jpg"
toprint_img = "/tmp/toprint.jpg"
rm_printimg_cmd = "rm -f /tmp/lomoprinting.jpg"
size_sql = "select picSize from machine where machine_id = " + machine_id
sel_sql = "select id, pic_path, content from weixin where machine_id = %s and consumer_code is not null and is_printed = 2"
upd_sql = "update weixin set is_printed = 1 where id = %s"
cp_offline_cmd = "cp /etc/lomotime/default/offline.jpg " + printing_img

big_or_small = None
logo_downloaded = False
printed = []

# db
conn = None

while True:
  try:

    # print "begin loop: " + time.ctime() # debug

    # check network connection
    is_network_ok = lomoutil.internet_on()
    if not is_network_ok:
      os.system(cp_offline_cmd)

    else:
      # get logo picture
      if not logo_downloaded:
        logo_cmd = "~/client/lomogetlogo.sh " + logo_imgurl
        logo_result = subprocess.check_output(logo_cmd, shell = True)
        if logo_result != "0":
          logo_downloaded = True
          #print "got logo image: " + time.ctime() # debug

      # connect db for the first time
      if conn == None:
        conn=MySQLdb.connect(host=db_host, user=db_usr, passwd=db_pwd, db=db_name, port=db_port, charset="utf8")
        conn.autocommit(True)

      # get pic size
      if big_or_small == None:
        cur = conn.cursor()
        cur.execute(size_sql)
        size = cur.fetchone() 
        if size[0] == None or "1" == size[0]:
          big_or_small = "S"
        else:
          big_or_small = "B"
        # print big_or_small # debug

      #print "db connected: " + time.ctime() # debug
  
      cur=conn.cursor()
      # query pictures to be printed
      cur.execute(sel_sql, [machine_id])
      rows = cur.fetchall()
      # print len(rows) # debug
      # print each picture
      for row in rows:
        row_id = row[0] # row id, for later use after printing
        pic = row[1] # picture path
        words = row[2] # bottom side words of the photo
        if pic is not None: 
          if pic in printed: # if already printed, skip it
            continue
          # check internet connection before download
          if not lomoutil.internet_on():
            break;
          # download picture to /tmp/toprint.jpg
          #download_cmd = "wget " + base_imgurl + pic + " -q -O " + toprint_img
          download_cmd = "~/client/lomodownload.sh " + base_imgurl + pic + " tmptoprint.jpg " + toprint_img
          # print download_cmd
          download_result = subprocess.check_output(download_cmd, shell = True)
          # print download_result
          if download_result != "0":
            # download failed, go to next picture
            continue

          #print "to run lomoprint.sh: " + time.ctime() # debug

          print_cmd = "~/client/lomoprint.sh " + big_or_small + " " + toprint_img
          if words is not None: 
            print_cmd = print_cmd + " '" + words + "'"
          # print print_cmd # debug
          print_result = subprocess.check_output(print_cmd, shell = True)
          # print "print result: " + print_result # debug

          #print "print finished: " + time.ctime() # debug

          if print_result == "0":
            # successfully printed, mark image printed, but check network first
            if lomoutil.internet_on():
              cur.execute(upd_sql, [str(row_id)])
            else:
              printed.append(pic)

            #print "db updated: " + time.ctime() # debug

          else:
            # cancel this time of printing
            time.sleep(600) # wait 10 minutes for error process
            break
          # time.sleep(pr_wait_sec) #uncessary
      os.system(rm_printimg_cmd)
      cur.close()
  except Exception, e:
    print e # debug
    os.system(rm_printimg_cmd)
  time.sleep(wait_sec)
# end wihle

