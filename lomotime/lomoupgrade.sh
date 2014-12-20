#!/bin/bash

base_url=$1

# clear new version folder, in case
rm -rf ~/client.new
rm -rf ~/client.bak
# create working folder
mkdir -p /tmp/lomo
cd /tmp/lomo

# get latest version and compare with current version
~/client/lomodownload.sh ${base_url}/VER lomover /tmp/lomo/VER > /dev/null 2>&1
#echo "current version: " #debug
#cat ~/client/VER #debug
#echo "new version: " #debug
#cat /tmp/lomo/VER #debug
#diff ~/client/VER /tmp/lomo/VER #debug
new_ver=`diff ~/client/VER /tmp/lomo/VER | wc -l`
#echo "if new version: ${new_ver}" #debug
if [ "${new_ver}" == "0" ]
then
  rm -rf /tmp/lomo
  echo -n 100
  exit 0
fi

# get new version package
~/client/lomodownload.sh ${base_url}/MD5 lomomd5 /tmp/lomo/MD5 > /dev/null 2>&1
~/client/lomodownload.sh ${base_url}/client.tar.gz lomoclient.tar.gz /tmp/lomo/client.tar.gz > /dev/null 2>&1
md5sum client.tar.gz > tmpmd5
#cat MD5 #debug
#cat tmpmd5 #debug
#diff MD5 tmpmd5 #debug
check_md5=`diff MD5 tmpmd5 | wc -l`
#echo "md5 check: ${check_md5}" #debug
if [ "${check_md5}" != "0" ] # download error
then
  rm -rf /tmp/lomo
  echo -n 1
  exit 0
fi

tar xzf client.tar.gz > /dev/null 2>&1
chmod 777 --silent -R client > /dev/null 2>&1
mv client ~/client.new
cd ~
rm -rf /tmp/lomo

if [ $? != 0 ] # something wrong, rollback
then 
  rm -rf ~/client.new
  echo -n 2
  exit 0
fi

echo -n 200
exit 0
