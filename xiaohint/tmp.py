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


def main():
    res = requests.post('http://127.0.0.1:5000/recommend', {'word': '游泳'})
    json_data = json.loads(res.content.decode('unicode_escape'))
    data = json_data['data']
    print(data)


if __name__ == '__main__':
    main()
