#!/usr/bin/env python

import memcache, requests, time

idfile = open('/etc/lomotime/machine_id', "r")
try:
    device_id = idfile.read().rstrip('\n')
finally:
    idfile.close()

infurl = "http://www.lomotime.cn/admin/mims/reg.do"
args = {"method": "getMachineConsumerCode", "machineCode": device_id}

shared = memcache.Client(['127.0.0.1:11211'], debug=0)

def get_consumer_code():
    req = requests.get(infurl, params = args)
    if req.status_code == 200:
        shared.set('ConsumerCode', req.text)

while True:
    get_consumer_code()
    time.sleep(2)

