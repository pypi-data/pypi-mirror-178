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

import hashlib
import os
import sys
import datetime
import requests
import pymongo
import pandas as pd
from pytdx.crawler.history_financial_crawler import HistoryFinancialCrawler
from qff.tools.local import download_path
from qff.tools.config import DATABASE
from qff.tools.utils import util_to_json_from_pandas

FINANCIAL_URL = 'http://down.tdx.com.cn:8001/tdxfin/gpcw.txt'


def calc_file_md5(filename):
    """
    计算文件的MD5值
    :param filename: 文件路径
    :return: str 文件的MD5值
    """
    with open(filename, mode='rb') as f:
        d = hashlib.md5()
        while True:
            # 128 is smaller than the typical filesystem block
            buf = f.read(4096)
            if not buf:
                break
            d.update(buf)
        return d.hexdigest()


def get_filename():
    """
    get_filename
    """
    return [(l[0], l[1])
            for l in [line.strip().split(",") for line in requests.get(FINANCIAL_URL).text.strip().split('\n')]]


def get_md5():
    return [l[1]
            for l in [line.strip().split(",") for line in requests.get(FINANCIAL_URL).text.strip().split('\n')]]


def download_report():
    """
    会创建一个download/文件夹
    """
    result = get_filename()
    res = []
    for item, md5 in result:
        if item in os.listdir(download_path) \
                and md5 == calc_file_md5('{}{}{}'.format(download_path, os.sep, item)):

            print('FILE {} is already in {}'.format(item, download_path))
        else:
            print('CURRENTLY GET/UPDATE {}'.format(item[0:12]))
            r = requests.get('http://down.tdx.com.cn:8001/tdxfin/{}'.format(item))
            file = '{}{}{}'.format(download_path, os.sep, item)

            with open(file, "wb") as code:
                code.write(r.content)
            res.append(item)
    return res


def get_and_parse(filename):
    with open(filename, 'rb') as df:
        data = HistoryFinancialCrawler().parse(download_file=df)

    if len(data) == 0:
        return None

    total_len = len(data[0])
    col = ['code', 'report_date']
    length = total_len - 2
    for i in range(0, length):
        col.append('00{}'.format(str(i + 1))[-3:])
    df = pd.DataFrame(data=data, columns=col)
    return df


def su_financial_files():
    """本地存储financialdata
    """
    res = download_report()

    coll = DATABASE.report
    coll.create_index(
        [("code", pymongo.ASCENDING), ("report_date", pymongo.ASCENDING)], unique=True)

    for item in res:
        if item[0:4] != 'gpcw':
            print(
                "file ", item, " is not start with gpcw , seems not a financial file , ignore!")
            continue
        date = int(item.split('.')[0][-8:])

        new_data = get_and_parse('{}{}{}'.format(download_path, os.sep, item))
        if new_data is None:
            continue

        print('QUANTAXIS NOW SAVING {}'.format(date))
        new_data = new_data.drop_duplicates(subset=['code', 'report_date'], keep='last')
        new_data = new_data.round(4)
        new_data = new_data.query('report_date == @date')
        cursor = coll.find(
            {'report_date': date},
            {"_id": 0},
        )
        db_data = pd.DataFrame([item0 for item0 in cursor])
        if len(db_data) > 0:
            ins_data = new_data[~new_data['code'].isin(db_data.code.to_list())]  # 更正前期报表数据不能保存
        else:
            ins_data = new_data
        if len(ins_data) > 0:
            print('即将新增的财报条数 {}'.format(len(ins_data)))
            try:
                coll.insert_many(util_to_json_from_pandas(ins_data), ordered=True)
            except Exception as e:
                print('批量新增失败，错误：{}，date:{}'.format(e, date))

        # TODO 处理前期报表数据修订的问题
        if len(db_data) > 0:
            lf_data = new_data[new_data['code'].isin(db_data.code.to_list())]
            # 取出pub_date
            upd_data = pd.concat([db_data, lf_data]).round(4)  # 保留4位小数
            upd_data = upd_data.drop_duplicates(keep=False).\
                drop_duplicates(subset=['code'], keep='last')

            if len(upd_data) > 0:
                upd_data = util_to_json_from_pandas(upd_data)
                try:
                    for d in upd_data:
                        coll.update_one({'code': d['code'], 'report_date': d['report_date']}, {'$set': d})
                except Exception as e:
                    print('批量更新失败，错误：{}，date:{}'.format(e, date))


    print('SUCCESSFULLY SAVE/UPDATE FINANCIAL DATA')


if __name__ == '__main__':
    su_financial_files()
