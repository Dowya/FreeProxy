import requests, random, re, time, socket, os
# from settings import XICI_API, User_Agent
from urllib.parse import urljoin
from lxml.html import etree
"""
西刺代理链接
"""
XICI_API = "http://www.xicidaili.com/nn/"
User_Agent ="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"

class proxy:
    def __init__(self):
        self.proxy_list =[]
        self.proxy_filter_list = []


    def get_proxy_from_xici(self):
        """
        获取为加工的代理
        :return:
        """

        headers = dict()
        headers["User-Agent"] = User_Agent
        for i in range(1,10):
            time.sleep(1)
            url = urljoin(XICI_API,str(i))
            res = requests.get(url=url,headers=headers).content
            sel = etree.HTML(text=res)
            trs = sel.xpath('//table[@id="ip_list"]/tr')
            for tr in trs[1:]:
                if tr.xpath("td[2]/text()"):
                    ip = tr.xpath('td[2]/text()')[0]
                    port = tr.xpath('td[3]/text()')[0]
                    ip_temp = '{}:{}'.format(ip,port)
                    print(ip_temp)
                    self.proxy_list.append(ip_temp)

    def filter_proxy(self):
        """
        验证ip
        :return:
        """
        socket.setdefaulttimeout(1)
        path = os.path.join(os.path.dirname(__file__),'./proxy_list')
        f = open(path, "w")
        head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
            'Connection': 'keep-alive'}
        url = "http://icanhazip.com"
        proxy_num = 0
        for proxy in self.proxy_list:
            proxy_temp = {"https": "https://{}".format(proxy)}
            try:
                req = requests.get(url, proxies=proxy_temp, timeout=2, headers=head).content
                print(req)
                write_proxy = proxy + "\n"
                f.write(write_proxy)
                proxy_num += 1
                self.proxy_filter_list.append(proxy)
            except Exception:
                print("代理链接超时，去除此IP：{0}".format(proxy))
                continue
        print("总共可使用ip量为{}个".format(proxy_num))
        f.close()
        return self.proxy_filter_list



if __name__ =="__main__":
    p = proxy()
    p.get_proxy_from_xici()
    p.filter_proxy()
