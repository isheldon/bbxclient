#!/usr/bin/env python
# -*- coding: utf-8 -*-

import memcache, requests, time
import lomoconf
import sys

reload(sys)
sys.setdefaultencoding( "utf-8" )

# read from config file
machine_id = lomoconf.machine_id()
wait_sec = lomoconf.consumer_code_interval()
info_url = lomoconf.info_url()
args = {"method": "getMachineConsumerCode", "mechineCode": machine_id}

shared = memcache.Client(['127.0.0.1:11211'], debug=0)

def get_consumer_code():
    req = requests.get(info_url, params = args)
    if req.status_code == 200:
        shared.set('ConsumerCode', req.text)
        print req.text

while True:
    try:
        get_consumer_code()
    except Exception, e:
        shared.set('ConsumerCode', '')
    time.sleep(wait_sec)

