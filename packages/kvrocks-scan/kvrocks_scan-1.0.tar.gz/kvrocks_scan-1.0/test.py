#coding:utf-8

import redis
import kvrocks_scan
kvrocks_instance = kvrocks_scan.repair(redis.StrictRedis(host="127.0.0.1",port=6379,db=0));

for k in kvrocks_instance.scan_iter("9*"):
	print(k);