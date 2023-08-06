### 起因
kvrocks的迭代命令(scan/sscan/zscan/hscan)返回的光标是字符串类型，而redis的光标是整数类型。 python的redis会将光标强制成int返回，所以会出现问题。
### 使用方法
很简单，就是把redis对象包一下

    import redis
    import kvrocks_scan
    kvrocks_instance = kvrocks_scan.repair(redis.StrictRedis(host="127.0.0.1",port=6379,db=0));
    
    for k in kvrocks_instance.scan_iter():
    	print(k);

