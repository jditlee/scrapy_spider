# -*- coding:utf-8 -*-
# author:凌陨心
# datetime:2023/6/1 14:26
# software: PyCharm

import requests, random
from datetime import datetime


class ProxyMiddleware(object):

    def getIP(self):
        a = requests.get("芝麻代理IP ").json().get('data')  # 芝麻代理IP
        b = []
        for i in a:
            IP = i.get("ip")
            PORT = i.get("port")
            IP_PROT = str(IP) + ":" + str(PORT)
            Expire_time = int(i.get("expire_time").split(" ")[1].replace(":", ""))
            now_time = int(str(datetime.now()).split('.')[0].split(" ")[1].replace(":", ""))
            if Expire_time < now_time:
                b.append(IP_PROT)
        h = len(b)
        if h != 0:
            num = random.randint(0, h - 1)
            c = b[num]
            thisProxy = {
                "https": "https://{}".format(c)
            }
            m = thisProxy.get('https')
            return m

    def process_request(self, request, spider):
        a = self.getIP()
        # request.meta['proxy'] = a
        return a
if __name__ == '__main__':
    proxymid = ProxyMiddleware()
    print(proxymid.getIP())