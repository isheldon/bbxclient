#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb, os, subprocess

idfile = open('/etc/bobox/device_id', "r")
try:
    machine_id = idfile.read().rstrip('\n')
finally:
    idfile.close()

base_imgurl = "http://122.225.105.20:8080/uploadImg/img/"
printing_img = "/tmp/lomoprinting.jpg"
sel_sql = "select id, pic_path from weixin where machine_id = %s and consumer_code is not null and is_printed = 2"
upd_sql = "update weixin set is_printed = 1 where id = %s"

# db
conn = None

while True:
  try:
    # connect db for the first time
    if conn == None:
      conn=MySQLdb.connect(host='122.225.105.22',user='heavenzyw',passwd='ywzywwei2008',db='lomo',port=3306)
  
    cur=conn.cursor()
    # query pictures to be printed
    cur.execute(sel_sql, machine_id)
    rows = cur.fetchall()
    # print each picture
    for row in rows:
      row_id = row[0] # row id, for later use after printing
      pic = row[1] # picture path
      if pic is not None: 
        # using wget to download picture to /tmp/lomoprinting.jpg
        download_cmd = "wget " + base_imgurl + pic + " -q -O " + printing_img
        os.system(download_cmd)
        # call java program to print image
        print_cmd = "java PrintImg " + printing_img
        print_result = subprocess.check_output(print_cmd, shell = True)
        if print_result == "0": # successfully printed
        cur.execute(upd_sql, str(row_id))
    cur.close()
  except MySQLdb.Error, e:
    print e
# end wihle

