# coding :utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2019 XuHaiJiang/QFF
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
 通达信下载的历史财报数据没有发布日期，通过在聚宽下载的数据，对数据库数据进行更新，增加财报公布日期
"""

import os

import pandas as pd

from QUANTAXIS.QAUtil import DATABASE
from QUANTAXIS.QAUtil.QASql import ASCENDING
from QUANTAXIS.QAUtil.QATransform import QA_util_to_json_from_pandas

from qff.tools.local import cache_path
import pickle


def patch_pub_date():
    backup_file = '{}{}{}'.format(cache_path, os.sep, 'pubdate.pkl')
    if os.path.exists(backup_file):
        with open(backup_file, 'rb') as pk_file:
            res: pd.DataFrame = pickle.load(pk_file)

        res['code'] = res['code'].map(lambda x: str(x)[0:6])
        res['statDate'] = res['statDate'].map(lambda x: int(''.join(x.split('-'))))

        coll = DATABASE.report
        coll.create_index(
            [("code", ASCENDING), ("pub_date", ASCENDING), ("report_date", ASCENDING)], unique=True)
        data = QA_util_to_json_from_pandas(res)
        for d in data:
            coll.update_one({'code': d['code'], 'report_date': d['statDate']},
                            {'$set': {'pub_date': d['pubDate']}})

        # 下面更新tdx有而聚宽中没有的财报数据
        cursor = coll.find({'pub_date': '2022-05-07'},
                           {"_id": 0, "code": 1, "pub_date": 1, "report_date": 1}
                           )
        df = pd.DataFrame([item0 for item0 in cursor])

        def modify_pub_date(s):
            tail = str(s)[-4:]
            year = int(s / 10000)
            if tail == "0331":
                return str(year) + "-04-28"
            elif tail == "0630":
                return str(year) + "-08-26"
            elif tail == "0930":
                return str(year) + "-10-29"
            elif tail == "1231":
                return str(year + 1) + "-04-28"

        df['pub_date'] = df['report_date'].apply(modify_pub_date)
        data = QA_util_to_json_from_pandas(df)
        for d in data:
            coll.update_one({'code': d['code'], 'report_date': d['report_date']},
                            {'$set': {'pub_date': d['pub_date']}})

