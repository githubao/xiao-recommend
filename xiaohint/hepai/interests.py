#!/usr/bin/env python
# encoding: utf-8

"""
@description:

@version: 1.0
@author: BaoQiang
@license: Apache Licence 
@contact: mailbaoqiang@gmail.com
@site: http://www.github.com/githubao
@software: PyCharm
@file: interests.py
@time: 2017/2/14 17:18
"""

import requests
import json
from xiaohint.pth import FILE_PATH

hepai_list_file = '{}/interests/interest_list.txt'.format(FILE_PATH)
hepai_item_file = '{}/interests/interest_item.txt'.format(FILE_PATH)

cate_dic = {}


def get_list():
    content = requests.get(list_url).content.decode()
    json_data = json.loads(content)

    for item in json_data['data']['list']:
        for subitem in item:
            cate_dic[int(subitem['type'])] = subitem['type_name']


def get_content():
    get_list()

    for i in range(11, 39):
        url = item_url_fmt.format(i)
        content = requests.get(url).content.decode()
        json_data = json.loads(content)
        for item in json_data['data']['type']:
            sub_cate_id = item['type']
            sub_cate_name = item['type_name']
            tags = item['data']

            tag_list = []
            for tag in tags:
                tag_name = tag['tag_name']
                tag_list.append(tag_name)

            with open(hepai_list_file, 'a', encoding='utf-8') as f1, open(hepai_item_file, 'a', encoding='utf-8') as f2:
                cate = cate_dic.get(i, None)
                f1.write('{}\t{}\t{}\t{}\n'.format(i, cate, sub_cate_id, sub_cate_name))
                for idx, item in enumerate(tag_list):
                    f2.write('{}\t{}\t{}\n'.format(sub_cate_id, '{}{:03d}'.format(sub_cate_id, idx+1), item))

            # break

        print('interests process {} complete'.format(i))

        # break


list_url = 'http://api2.quhepai.com/interests/list?sa=Z3xKVy7sF8I2L2MvgHCS9BfYuBg/yuKOXnX3M7e5AO6XvX4kbzs0QoFtc4VAr6rLsNgKQeq8fZVitZ/LVckJfS7HAo2n4RSbH//7qj/%2BLRN7v8MF/IhWcMxT08Cg9NIlRuyk4dxeEGYfgQTRTrssGey7xu826M1RxMXZ5eUEj7U%3D&nonce=1487063368465&isopenudid=0&long=116.310964&user_id=27917730&area_id=110000&lat=40.027542&token=8f9B1raSVNaiPsAKq5e1whICIGWe0jAi_1487042677&imei=2662392A-5A0E-4877-A1EC-03E69A589732&ver=1.4.8&sv=iPhone%20OS%209.3&ch=iOS&api=16&model=iPhone%206s&build=6956&from=1'
item_url_fmt = 'http://api2.quhepai.com/interests/detail?sa=INC2pUR6RbXcpk7HaId1121NYnMvTLlLtnJba2dmxXY3aecBe1aCcKgKZ7lrEpMT85nxqiK5jjdfmvmPFlcSTf8M%2BeXLRGlg4FNIuJT2jA0qqdHA0S488V0T2WJo52ZLVjHgHwC1Vvc7jmslFxVZ1gk30Li2bco251Uij7QCbDs%3D&nonce=1487063278127&isopenudid=0&long=116.310964&user_id=27917730&area_id=110000&lat=40.027542&token=8f9B1raSVNaiPsAKq5e1whICIGWe0jAi_1487042677&imei=2662392A-5A0E-4877-A1EC-03E69A589732&ver=1.4.8&sv=iPhone%20OS%209.3&ch=iOS&api=16&model=iPhone%206s&build=6956&type={}'


def main():
    get_content()


if __name__ == '__main__':
    main()
