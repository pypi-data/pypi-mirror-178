#!/opt/conda/bin/python

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
保存通达信财报数据
"""


import os
import pandas as pd
import pymongo
from QUANTAXIS.QAFetch.QAfinancial import (download_financialzip, parse_filelist, download_financialzip_fromtdx)
from QUANTAXIS.QASetting.QALocalize import download_path
from QUANTAXIS.QAUtil import DATABASE
from QUANTAXIS.QAUtil.QASql import ASCENDING
from QUANTAXIS.QAUtil.QATransform import QA_util_to_json_from_pandas


def su_financial_files(fromtdx=False):
    """本地存储financialdata
    """
    if fromtdx:
        res = download_financialzip_fromtdx()
    else:
        res = download_financialzip()

    coll = DATABASE.report
    coll.create_index(
        [("code", ASCENDING), ("report_date", ASCENDING)], unique=True)

    # for item in res:
    for item in os.listdir(download_path):
        if item[0:4] != 'gpcw':
            print(
                "file ", item, " is not start with gpcw , seems not a financial file , ignore!")
            continue
        date = int(item.split('.')[0][-8:])
        print('QUANTAXIS NOW SAVING {}'.format(date))
        print('在数据库中的条数 {}'.format(coll.find({'report_date': date}).count()))
        try:
            data = QA_util_to_json_from_pandas(parse_filelist([item]).reset_index(
            ).drop_duplicates(subset=['code', 'report_date']).sort_index())
            print('即将更新的条数 {}'.format(len(data)))
            # data["crawl_date"] = str(datetime.date.today())
            try:
                for d in data:
                    coll.update_one({'code': d['code'], 'report_date': d['report_date']}, {'$set': d}, upsert=True)

            except Exception as e:
                if isinstance(e, MemoryError):
                    coll.insert_many(data, ordered=True)
                elif isinstance(e, pymongo.bulk.BulkWriteError):
                    pass
        except Exception as e:
            print('似乎没有数据')

    print('SUCCESSFULLY SAVE/UPDATE FINANCIAL DATA')


if __name__ == '__main__':
    su_financial_files()
