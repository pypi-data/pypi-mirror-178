#!/opt/conda/bin/python

#coding :utf-8

import datetime
import numpy as np
import pandas as pd
import QUANTAXIS as QA
import pymongo
from QUANTAXIS.QAUtil import (
    DATABASE,
    QA_util_get_pre_trade_date,
    QA_util_get_next_trade_date,
    QA_util_log_info,
    QA_util_to_json_from_pandas,
    QA_util_code_tolist,
    QA_util_date_valid
)


def save_stock_day_full(code, err):
    """
    保存完整的日线数据，包括：股票代码，日期，OHCL价格，成交量，成交金额，量比(qrr)，换手率(tr)，市盈率(pe)，
    市净率（pb),市值(mc)等
    """
    try:
        # 首选查找数据库 是否 有 这个股票代码的数据
        ref1 = DATABASE.stock_day_full.find({"code": str(code)[0:6]}, sort=[("date", -1)]).limit(1)
        start = QA_util_get_next_trade_date(ref1[0]["date"], 1) if ref1.count() > 0 else '2000-01-04'

        # 查询股票日数据，读取开始日期前5天的数据，用于计算量比
        ref2 = DATABASE.stock_day.find(
            {
                "code": str(code)[0:6],
                "date":
                    {
                        "$gte": QA_util_get_pre_trade_date(start, 6)
                    }
            }
        )
        if ref2.count() < 6:
            raise ValueError("查询股票日数据无返回！")
        end = ref2[ref2.count() - 1]["date"]
        if start > end:
            raise ValueError("stock_day_full数据已更新！")

        # 从数据库中读取财务数据
        ref3 = DATABASE.financial.find(
            {
                "code": str(code)[0:6],
                "report_date":
                    {
                        "$gte": int(start[0:4] + start[5:7] + start[8:10]) - 10000
                    }
            },
            {
                "_id": 0,
                "report_date": 1,
                "001": 1,  # 每股收益
                "004": 1,  # 每股净资产
                "238": 1  # 总股本
            }
        )
        if ref3.count() <= 0:
            raise ValueError("无对应的财务数据！")

        # 开始计算
        QA_util_log_info(
            'UPDATE_STOCK_DAY_FULL \n Trying updating {} from {} to {}'
                .format(code,
                        start,
                        end)
        )
        res = pd.DataFrame([item for item in ref2])
        res = res.loc[:, ['code', 'date', 'open', 'high', 'low', 'close', 'vol', 'amount']].set_index('date')
        # 计算量比
        res['qrr'] = np.around(res.vol / res.vol.rolling(5).mean().shift(1), 2)
        # 计算涨幅
        res['pct'] = np.around(res.close/res.close.shift(1)-1, 4)
        res['eps'] = np.NaN  # 每股收益
        res['aps'] = np.NaN  # 每股净资产
        res['tc'] = np.NaN  # 总股本

        fin = pd.DataFrame([item for item in ref3])
        fin["date"] = fin["report_date"].apply(
            lambda x: datetime.datetime.strptime(str(x), '%Y%m%d').strftime('%Y-%m-%d'))
        fl = len(fin)
        for i in range(1, fl - 1):
            res.loc[fin.date[i - 1]:fin.date[i], ['eps', 'aps', 'tc']] = [
                fin['001'][i - 1] * 12 / int(fin.date[i - 1][5:7]),
                fin['004'][i - 1],
                fin['238'][i - 1]]

        res.loc[fin.date[fl - 1]:, ['eps', 'aps', 'tc']] = [fin['001'][fl - 1] * 12 / int(fin.date[fl - 1][5:7]),
                                                            fin['004'][fl - 1],
                                                            fin['238'][fl - 1]]

        # 计算换手率(tr)，市盈率(pe)，市净率（pb),市值(mc)
        res['vol'] = res['vol'] * 100
        res['tr'] = np.around(res['vol'] / res['tc'], 4)
        res['pe'] = np.around(res['close'] / res['eps'], 2)
        res['pb'] = np.around(res['close'] / res['aps'], 2)
        res['mc'] = np.around(res['close'] * res['tc'] / 1.0e+8, 2)

        res = res.loc[start:end, ['code', 'open', 'high', 'low', 'close', 'vol',
                                  'amount', 'pct', 'qrr', 'tr', 'pe', 'pb', 'mc']]

        DATABASE.stock_day_full.insert_many(
            QA_util_to_json_from_pandas(
                res.reset_index()
            )
        )

    except Exception as error0:
        print(error0)
        print(code)
        err.append(str(code))

    return


def su_stock_day_full(client=DATABASE):
    stock_list = QA.QA_fetch_stock_list().index.to_list()
    coll_stock_day_full = client.stock_day_full
    coll_stock_day_full.create_index(
        [("code",
          pymongo.ASCENDING),
         ("date",
          pymongo.ASCENDING)]
    )
    err = []

    for item in range(len(stock_list)):
        QA_util_log_info('The {} of Total {}'.format(item, len(stock_list)))
        save_stock_day_full(stock_list[item], err)

    if len(err) < 1:
        QA_util_log_info('SUCCESS save stock day full ^_^')
    else:
        QA_util_log_info('ERROR CODE \n ')
        QA_util_log_info(err)
    return


def  su_data_by_day(coll_src, coll_dest, uni=True):
    """ 按天将源数据集数据保存至数据库   """
    try:
        cursor = coll_src.find(
            {},
            {"_id": 0},
        )
        df = pd.DataFrame([item for item in cursor])
        df["gen_date"] = datetime.datetime.now().strftime('%Y-%m-%d')

        coll_dest.create_index(
            [("gen_date",
              pymongo.ASCENDING),
             ("code",
              pymongo.ASCENDING)], unique=uni
        )
        coll_dest.insert_many(
            QA_util_to_json_from_pandas(df)
        )
        return True
    except Exception as error0:
        print(error0)
        return False


def su_stock_list_hist():
    QA_util_log_info('START save stock list history data...')
    if su_data_by_day(DATABASE.stock_list, DATABASE.stock_list_hist):
        QA_util_log_info('SUCCESS save stock list history data ^_^')
    return

 

def su_stock_info_hist():
    QA_util_log_info('START save stock info history data...')
    if su_data_by_day(DATABASE.stock_info, DATABASE.stock_info_hist):
        QA_util_log_info('SUCCESS save stock info history data ^_^')
    return


def su_stock_block_hist():
    QA_util_log_info('START save stock block history data...')
    if su_data_by_day(DATABASE.stock_block, DATABASE.stock_block_hist, uni=False):
        QA_util_log_info('SUCCESS save stock block history data ^_^')
    return


def get_stock_day_full(code=None, start_date=None, end_date=None, count=None):
    if end_date is None:
        end_date = datetime.datetime.now().strftime('%Y-%m-%d')
    if start_date is None:
        if count is None:
            start_date = end_date
        else:
            start_date = QA_util_get_pre_trade_date(end_date, count)

    start = str(start_date)[0:10]
    end = str(end_date)[0:10]
    # code checking
    if code is None:
        cursor = DATABASE.stock_day_full.find(
            {
                "date": {
                    "$lte": end,
                    "$gte": start
                }
            },
            {"_id": 0},
            batch_size=10000
        )
    else:
        code = QA_util_code_tolist(code)
        cursor = DATABASE.stock_day_full.find(
            {
                'code': {
                    '$in': code
                },
                "date": {
                    "$lte": end,
                    "$gte": start
                    }
            },
            {"_id": 0},
            batch_size=10000
        )
    res = pd.DataFrame([item for item in cursor])
    try:
        res = res.drop_duplicates((['date', 'code']))\
            .query('vol>1')\
            .set_index(['code', 'date'])
    except Exception as error0:
        print(error0)
        res = None

    return res


def su_stock_name():
    try:
        cursor = DATABASE.stock_list.find(
            {},
            {"_id": 0, "code": 1, "name": 1},
        )
        df1 = pd.DataFrame([item for item in cursor])
        df1 = df1.set_index('code')

        cursor = DATABASE.stock_info.find(
            {},
            {"_id": 0, "code": 1, "ipo_date": 1},
        )
        df2 = pd.DataFrame([item for item in cursor])
        df2 = df2.set_index('code')

        df3 = df1.join(df2, how="left")
        df4: pd.DataFrame = df3[df3['ipo_date'] > 0]
        df4 = df4.reset_index()
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        
        df4.insert(0, 'date', value=today)
        df4.drop('ipo_date', axis=1, inplace=True)
        coll = DATABASE.stock_name
        coll.create_index(
            [("date",
              pymongo.ASCENDING),
             ("code",
              pymongo.ASCENDING)],
            unique=True
        )
        coll.insert_many(
            QA_util_to_json_from_pandas(df4)
        )
        print("save stock name sucessed!")
        return True
    except Exception as error0:
        print(error0)
        return False



# if __name__ == '__main__':
#     su_stock_day_full()
#     su_stock_list_hist()
#     su_stock_info_hist()
#     su_stock_block_hist()
#     su_stock_name()

