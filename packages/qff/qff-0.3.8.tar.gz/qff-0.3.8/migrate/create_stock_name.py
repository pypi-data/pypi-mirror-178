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

# 根据聚宽下载的股票简称变更历史数据，创建自己的股票历史名称库

import os
import pandas as pd
import datetime
from QUANTAXIS.QAUtil import DATABASE
from QUANTAXIS.QAUtil.QASql import ASCENDING
from QUANTAXIS.QAUtil.QATransform import QA_util_to_json_from_pandas

from qff.tools.local import cache_path
# from qff.tools.query import *
from qff.tools.date import get_trade_days
import pickle


def create_stock_name_db():
    backup_file = '{}{}{}'.format(cache_path, os.sep, 'stockname.pkl')
    if os.path.exists(backup_file):
        with open(backup_file, 'rb') as pk_file:
            res: pd.DataFrame = pickle.load(pk_file)
        res = res.set_index('id').reset_index()
        res['code'] = res['code'].map(lambda x: str(x)[0:6])
        res['start_date'] = res['start_date'].map(lambda x:pd.Timestamp(x).strftime("%Y-%m-%d"))

        res = res[['code','start_date','new_name']]
        # 发现退市股票没有，以现在的股票来匹配
        collections = DATABASE.stock_info
        cursor = collections.find(
            {},
            {"_id": 0, "code": 1, 'ipo_date':1},
        )
        stocks = {item["code"]: item["ipo_date"] for item in cursor}

        # today = str(pd.Timestamp.today())[:10]
        today = '2022-05-07'
        df_list = []
        for code, ipo in stocks.items():
            print(code)
            if len(str(ipo)) != 8:
                continue
            ipodate = datetime.datetime.strptime(str(ipo), '%Y%m%d').strftime('%Y-%m-%d')
            date_list = get_trade_days(ipodate, today)
            # df = pd.DataFrame([{'date': item, 'code':code} for item in date_list])
            # df = df.set_index('date')
            df = pd.DataFrame({'code':[code]*len(date_list), 'name':[None]*len(date_list)},
                              index=pd.Index(date_list, dtype=str, name='date'))
            fin = res[res['code'] == code].copy().reset_index(drop=True)
            if len(fin) > 0:
                for i in range(0, len(fin)):
                    start = fin.start_date[i]
                    if start < df.index[0]:
                        start = df.index[0]
                    df.loc[start, 'name'] = fin.new_name[i]
                df = df.reset_index()
                df = df.fillna(method='ffill')
                df = df.fillna(method='bfill')
                df_list.append(df)

        df_sn = pd.concat(df_list)
        df_sn = df_sn.sort_values(['date', 'code'])
        coll = DATABASE.stock_name
        coll.create_index(
            [("date", ASCENDING), ("code", ASCENDING)], unique=True)
        data = QA_util_to_json_from_pandas(df_sn)
        coll.insert_many(data, ordered=False)

        print("stock_name数据库更新成功！")


# 处理退市股票
def patch_tuishi_stock():
    backup_file = '{}{}{}'.format(cache_path, os.sep, 'stockname.pkl')
    if os.path.exists(backup_file):
        with open(backup_file, 'rb') as pk_file:
            res: pd.DataFrame = pickle.load(pk_file)
        res = res.set_index('id').reset_index()
        res['code'] = res['code'].map(lambda x: str(x)[0:6])
        res['start_date'] = res['start_date'].map(lambda x:pd.Timestamp(x).strftime("%Y-%m-%d"))
        res = res[['code', 'start_date', 'new_name']]
    else:
        print('error1')
        raise

    backup_file = '{}{}{}'.format(cache_path, os.sep, '退市股票.pkl')
    if os.path.exists(backup_file):
        with open(backup_file, 'rb') as pk_file:
            ts: pd.DataFrame = pickle.load(pk_file)
        ts = ts.reset_index().rename(columns={'indicator':'code'})
        ts['code'] = ts['code'].map(lambda x: str(x)[0:6])
        ts['start_date'] = ts['start_date'].map(lambda x:pd.Timestamp(x).strftime("%Y-%m-%d"))
        ts['end_date'] = ts['end_date'].map(lambda x: pd.Timestamp(x).strftime("%Y-%m-%d"))
        ts = ts[['code', 'start_date', 'end_date']]
    else:
        print('error2')
        raise

    df_list = []
    for index, row in ts.iterrows():
        print(row.code)
        code = row.code
        date_list = get_trade_days(row.start_date, row.end_date)
        df = pd.DataFrame({'code':[code]*len(date_list), 'name':[None]*len(date_list)},
                          index=pd.Index(date_list, dtype=str, name='date'))
        fin = res[res['code'] == code].copy().reset_index(drop=True)
        if len(fin) > 0:
            for i in range(0, len(fin)):
                start = fin.start_date[i]
                if start < df.index[0]:
                    start = df.index[0]
                df.loc[start, 'name'] = fin.new_name[i]
            df = df.reset_index()
            df = df.fillna(method='ffill')
            df = df.fillna(method='bfill')
            df_list.append(df)
        else:
            print('股票代码在名称库未找到{}'.format(code))

    df_sn = pd.concat(df_list)
    df_sn = df_sn.sort_values(['date', 'code'])
    coll = DATABASE.stock_name
    coll.create_index(
        [("date", ASCENDING), ("code", ASCENDING)], unique=True)
    data = QA_util_to_json_from_pandas(df_sn)
    coll.insert_many(data, ordered=False)

    print("stock_name数据库更新成功！")


if __name__ == '__main__':
    create_stock_name_db()
