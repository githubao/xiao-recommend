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
@file: interests_svr.py
@time: 2017/2/14 18:56
"""

from xiaohint.pth import *
from flask import request, Flask
from xiaohint.hepai import interests_recommend
import json

app = Flask(__name__)


@app.route('/recommend', methods=['POST'])
def recommend():
    word = request.form.get('word')
    res = interests_recommend.recommend(word)
    logging.info('[{}]->[{}]'.format(word, res))
    data = {'data': res}
    return app.make_response((json.dumps(data), 200))


@app.route('/')
def index():
    return 'interests score run'


if __name__ == '__main__':
    app.run()
