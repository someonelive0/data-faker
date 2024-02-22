# -*- coding: utf-8 -*-
import requests, binascii
from requests import Request, Session
from urllib.parse import urlparse


url = 'http://localhost:3000/xxx'
# response = requests.get('http://api.github.com')

# print(response.status_code)
# print(response.text)

def request2bin(prepped):
    o = urlparse(prepped.url)
    s = '%s %s HTTP/1.1\r\n' % (prepped.method, prepped.path_url)
    s += 'Host: %s\r\n' % o.hostname
    for h in prepped.headers:
        s += '%s: %s\r\n' % (h, prepped.headers[h])
    if prepped.body is not None:
        s += '\r\n'
        s += prepped.body
    return s.encode('utf-8')

def response2bin(resp):
    s = 'HTTP/1.1 %s %s\r\n' % (resp.status_code, resp.reason)
    for h in resp.headers:
        s += '%s: %s\r\n' % (h, resp.headers[h])
    if resp.text is not None:
        s += '\r\n'
        s += resp.text
    return s.encode('utf-8')


s = Session()
req = Request('GET', url)
prepped = s.prepare_request(req)
print(request2bin(prepped))

# Merge environment settings into session
settings = s.merge_environment_settings(prepped.url, {}, None, None, None)
resp = s.send(prepped, **settings)
print(response2bin(resp))

