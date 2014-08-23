#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb, os, subprocess, time, requests
import lomoconf

# read from config file
machine_id = lomoconf.machine_id()
base_imgurl = lomoconf.img_base_url()
db_host = lomoconf.db_host()
db_usr = lomoconf.db_usr()
db_pwd = lomoconf.db_pwd()
db_name = lomoconf.db_name()
db_port = lomoconf.db_port()
wait_sec = lomoconf.print_interval()
pr_wait_sec = lomoconf.current_print_interval()
checkUrl = lomoconf.check_url()

printing_img = "/tmp/lomoprinting.jpg"
rm_printimg_cmd = "rm -f /tmp/lomoprinting.jpg"
sel_sql = "select id, pic_path, content from weixin where machine_id = %s and consumer_code is not null and is_printed = 2"
upd_sql = "update weixin set is_printed = 1 where id = %s"
cp_offline_cmd = "cp /etc/lomotime/default/offline.jpg " + printing_img

# db
conn = None

while True:
  try:
    # check network connection
    is_network_ok = True
    try:
      requests.get(checkUrl)
    except Exception, e: # the network is not fine
      is_network_ok = False
      os.system(cp_offline_cmd)

    if is_network_ok:

      # connect db for the first time
      if conn == None:
        conn=MySQLdb.connect(host=db_host, user=db_usr, passwd=db_pwd, db=db_name, port=db_port)
  
      cur=conn.cursor()
      # query pictures to be printed
      cur.execute(sel_sql, [machine_id])
      rows = cur.fetchall()
      # print len(rows)
      # print each picture
      for row in rows:
        row_id = row[0] # row id, for later use after printing
        pic = row[1] # picture path
        words = row[2] # bottom side words of the photo
        if pic is not None: 
          # using wget to download picture to /tmp/lomoprinting.jpg
          download_cmd = "wget " + base_imgurl + pic + " -q -O " + printing_img
          os.system(download_cmd)
          # call java program to print image
          print_cmd = "java PrintImage " + printing_img
          if words is not None: 
            print_cmd = print_cmd + " '" + words + "'"
          # print print_cmd
          print_result = subprocess.check_output(print_cmd, shell = True)
          # print "print result: " + print_result
          if print_result == "0": # successfully printed
            cur.execute(upd_sql, [str(row_id)])
          time.sleep(pr_wait_sec)
      os.system(rm_printimg_cmd)
      cur.close()
  except Exception, e:
    print e
    os.system(rm_printimg_cmd)
  time.sleep(wait_sec)
# end wihle

