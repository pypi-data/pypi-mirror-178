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
import os
from qff import *
import pandas as pd
import pickle
import pymongo
import datetime


def find_lost_data():
    coll = DATABASE.stock_min
    cursor = coll.find(
        {
            "type": "1min",
            "code": "000001"
        },
        {"_id": 0, "datetime": 1}
    )
    df = pd.DataFrame([item for item in cursor])
    df["date"] = df["datetime"].apply(lambda x: str(x)[0:10])
    s1 = df.date.unique().tolist()
    s2 = get_trade_days(s1[0], s1[-1])
    a = list(set(s2).difference(set(s1)))
    # 按列表中日期查询一下当天09：37分有没有数据，从数据库中直接查询
    # 有的话形成一个字典，保存该日期有分钟数据的股票
    b = [util_time_stamp(str(i) + ' 09:37:00') for i in a]
    coll = DATABASE.stock_min
    cursor = coll.find(
        {
            "type": "1min",
            "timestamp": {
                '$in': b
            },
        },
        {"_id": 0, "code": 1, "datetime": 1}
    )
    df1 = pd.DataFrame([item for item in cursor])
    # if len(df1)>0:

    #
    # with open('min_data_file', 'wb') as pk_file:
    #     pickle.dump(a, pk_file)


def patch_min_data(datafile):
    # datafile = 'min_data_2019-09-23'
    if not os.path.exists(datafile):
        print("Data File Not Be Find!:{}".format(datafile))
        return

    with open(datafile, 'rb') as pk_file:
        data: pd.DataFrame = pickle.load(pk_file)

    data['time'] = data['time'].apply(lambda x: str(x))
    data['code'] = data['code'].apply(lambda x: str(x)[:6])
    data.rename(columns={'time': 'datetime', 'volume': 'vol', 'money': 'amount'}, inplace=True)
    df = data[['open', 'close', 'high', 'low', 'vol', 'amount', 'datetime', 'code']]
    df = df.assign(
        date=df['datetime'].apply(lambda x: str(x)[:10]),
        date_stamp=df['datetime'].apply(lambda x: util_time_stamp(x[:10])),
        time_stamp=df['datetime'].apply(lambda x: util_time_stamp(x)),
        type='1min'
    )

    coll = DATABASE.stock_min
    coll.create_index(
        [
            ('code',
             pymongo.ASCENDING),
            ('time_stamp',
             pymongo.ASCENDING),
            ('date_stamp',
             pymongo.ASCENDING)
        ]
    )
    coll.insert_many(
        util_to_json_from_pandas(df)
    )
    print("分钟数据文件保存成功！")


if __name__ == '__main__':
    with open('data/min_data_file', 'rb') as pk_file:
        a: list = pickle.load(pk_file)
        a.sort()
        # b = a[2:43]
        # b = a[43:73]
        b = a[73:93]
    for date in b:
        filename = '../min_data_' + str(date)
        print(filename)
        _time = datetime.datetime.now()
        patch_min_data(filename)
        print(datetime.datetime.now() - _time)
