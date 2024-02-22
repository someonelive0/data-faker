# -*- coding: utf-8 -*-
# 产生模拟http pcap文件，方法是访问本地 faka_api，然后把请求和响应保存成pcap文件

import mkpcap_http
import random, time, sys, logging, argparse, socket
from requests import Request, Session
from urllib.parse import urlparse


logger = logging.getLogger('fake_pcap')
ARG_TABLE_NUMBER = 2
ARG_ITEM_MIN = 20
ARG_ITEM_MAX = 100
ARG_DB = 'mysql'
ARG_INSERT_BENTCH = 40


def init():
    logger.setLevel(logging.DEBUG)
    formator = logging.Formatter(fmt="%(asctime)s [ %(filename)s ]  %(lineno)d行 | [ %(levelname)s ] | [%(message)s]", datefmt="%Y/%m/%d/%X")
    sh = logging.StreamHandler()
    fh = logging.FileHandler("fake_pcap.log", encoding="utf-8")
    sh.setFormatter(formator)
    fh.setFormatter(formator)
    logger.addHandler(sh)
    logger.addHandler(fh)

def request2str(prepped, hostname):
    s = '%s %s HTTP/1.1\r\n' % (prepped.method, prepped.path_url)
    s += 'Host: %s\r\n' % hostname
    for h in prepped.headers:
        s += '%s: %s\r\n' % (h, prepped.headers[h])
    if prepped.body is not None:
        s += '\r\n'
        s += prepped.body
    return s

def response2str(resp):
    s = 'HTTP/1.1 %s %s\r\n' % (resp.status_code, resp.reason)
    for h in resp.headers:
        s += '%s: %s\r\n' % (h, resp.headers[h])
    if resp.text is not None:
        s += '\r\n'
        s += resp.text
    return s

def http_access(url, hostname):
    s = Session()
    req = Request('GET', url)
    prepped = s.prepare_request(req)
    str_req = request2str(prepped, hostname)

    # Merge environment settings into session
    settings = s.merge_environment_settings(prepped.url, {}, None, None, None)
    resp = s.send(prepped, **settings)
    str_resp = response2str(resp)

    return str_req, str_resp


# 主函数
if __name__ == '__main__':
    init()

    url = 'http://localhost:3000/xxx'
    o = urlparse(url)
    dip = socket.gethostbyname(o.hostname)

    # 执行HTTP访问，把请求和响应拼接成HTTP协议的字符串
    str_req, str_resp = http_access(url, o.hostname)

    # 把请求和响应拼接成HTTP协议的字符串，写入到pcap文件，并指定目的IP和端口
    mkpcap_http.mk_http_pcap(http_request=str_req, http_response=str_resp, dst_ip=dip, dst_port=o.port, pcapname=r'http')
