#!/usr/bin/env python
# encoding: utf-8

"""
@description: 对外提供服务

@version: 1.0
@author: BaoQiang
@license: Apache Licence 
@contact: mailbaoqiang@gmail.com
@site: http://www.github.com/githubao
@software: PyCharm
@file: buluo_srv.py
@time: 2017/1/16 21:06
"""

from xiaohint.pth import *
from flask import request, Flask
from xiaohint.buluo import cate_rank
import json

app = Flask(__name__)


@app.route('/recommend', methods=['POST'])
def recommend():
    word = request.form.get('word')
    res = cate_rank.recommend(word)
    logging.info('[{}]->[{}]'.format(word, res))
    data = {'data':res}
    return app.make_response((json.dumps(data), 200))


@app.route('/')
def index():
    return 'buluo score run'


if __name__ == '__main__':
    app.run()
