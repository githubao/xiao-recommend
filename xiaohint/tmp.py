#!/usr/bin/env python
# encoding: utf-8

"""
@description: 临时文件

@version: 1.0
@author: BaoQiang
@license: Apache Licence 
@contact: mailbaoqiang@gmail.com
@site: http://www.github.com/githubao
@software: PyCharm
@file: tmp.py
@time: 2017/1/11 20:46
"""

import requests
import json
from collections import OrderedDict

def tmp():
    url = 'http://cgi.find.qq.com/qqfind/buddy/search_v3'
    data = {'sex': '0', 'hdistrict': '0', 'hprovince': '0', 'firston': '1', 'ldw': '1068805307', 'province': '11',
            'city': '0', 'agerg': '0', 'country': '1', 'online': '1', 'keyword': '97123687', 'sessionid': '0',
            'hcountry': '1', 'hcity': '0', 'num': '20', 'video': '0', 'district': '0', 'page': '0'}
    cookies = {'pt2gguin': 'o0779439458', 'ptisp': 'ctc', 'itkn': '1780992046', 'skey': 'Zs63Xl1QrW', 'RK': 'GX0P9Rk+e4', 'ptcz': '8b6dfb1adb6ab7e170264682e2b1b64b545053cec8e3ccd248c19eb5ca7e75ab', 'uin': 'o779439458', 'pgv_pvid': '3960994630'}

    res = requests.post(url, data,headers={'referer':'http://find.qq.com/'},cookies=cookies)
    print(res.content.decode())


def tmp2():
    s = 'num=20&page=0&sessionid=0&keyword=97123687&agerg=0&sex=0&firston=1&video=0&country=1&province=11&city=0&district=0&hcountry=1&hprovince=0&hcity=0&hdistrict=0&online=1&ldw=1980579370'
    s = 'RK=GX0P9Rk+e4; pgv_pvid=3960994630; ptisp=ctc; ptcz=8b6dfb1adb6ab7e170264682e2b1b64b545053cec8e3ccd248c19eb5ca7e75ab; pt2gguin=o0779439458; itkn=1780992046; uin=o779439458; skey=Zs63Xl1QrW'
    dic = {}
    # dic = OrderedDict()
    # attr = s.split('&')
    attr = s.split('; ')
    for item in attr:
        key, value = item.split('=')
        dic[key] = value
    print(dic)


def tmp1():
    res = requests.post('http://127.0.0.1:5000/recommend', {'word': '游泳'})
    json_data = json.loads(res.content.decode('unicode_escape'))
    data = json_data['data']
    print(data)


if __name__ == '__main__':
    tmp()
