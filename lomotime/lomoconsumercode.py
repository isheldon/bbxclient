#!/usr/bin/env python

import memcache, requests, time
import lomoconf

machine_id = lomoconf.machine_id()

infurl = "http://www.lomotime.cn/admin/mims/reg.do"
args = {"method": "getMachineConsumerCode", "machineCode": machine_id}

shared = memcache.Client(['127.0.0.1:11211'], debug=0)

def get_consumer_code():
    req = requests.get(infurl, params = args)
    if req.status_code == 200:
        shared.set('ConsumerCode', req.text)

while True:
    get_consumer_code()
    time.sleep(2)

