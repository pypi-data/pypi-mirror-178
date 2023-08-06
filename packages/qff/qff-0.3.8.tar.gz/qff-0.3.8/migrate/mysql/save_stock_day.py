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
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir)))

import pandas as pd

from initdb import *
from qff.price.fetch import fetch_stock_list, fetch_price
from qff.tools.date import run_time, get_real_trade_date, get_next_trade_day
from qff.tools.logs import log
import datetime


def now_time():
    return str(get_real_trade_date(str(datetime.date.today() - datetime.timedelta(days=1)))) + \
           ' 17:00:00' if datetime.datetime.now().hour < 15 \
           else str(get_real_trade_date(str(datetime.date.today()))) + ' 15:00:00'


@run_time
def save_stock_list(market='stock'):  # 速度快很多
    """
    从通达信获取股票/指数/ETF列表，并保存到mysql数据库中
    :param market: 市场类型，目前支持“stock/index/etf", 默认“stock".
    :return:
    """
    table_name = market+'_list'
    df = fetch_stock_list(market).reset_index()
    data = [tuple(x) for x in df.to_records(index=False)]

    with mysql() as cursor:
        cursor.execute(f" DELETE FROM {table_name}; ")
        # cursor.execute(" TRUNCATE TABLE stock_list; ")
        sql = f"insert into {table_name} values " + str(data)[1:-1]
        cursor.execute(sql)

    log.info(f"save_stock_list({market}) run finished!")


# @run_time
# def save_stock_day(market='stock'):
#     """
#     从通达信获取交易日数据，并保存到mysql数据库中
#     :param market: 市场类型，目前支持“stock/index/etf", 默认“stock".
#     """
#
#     stock_list = fetch_stock_list(market).index.to_list()
#     end_date = now_time()[:10]
#     table_name = market+'_day'
#     max_date = mysql_2_df(f"SELECT code, MAX(date) as max_date FROM {table_name} GROUP BY code")
#     if max_date is not None and len(max_date) > 0:
#         max_date = max_date.set_index('code')
#
#     data_num = 0
#     data_list = []
#     for item in range(len(stock_list)):
#         log.info('SAVE_{}_day : The {} of Total {}'.format(market, item, len(stock_list)))
#         code = stock_list[item]
#         if max_date is None or code not in max_date.index:
#             start_date = '1991-01-01'
#         else:
#             start_date = str(max_date.loc[code, 'max_date'])[:10]
#
#         if start_date != end_date:
#             start_date = get_next_trade_day(start_date)
#             log.info('Trying updating {} from {}'.format(code, start_date))
#             data = fetch_price(code, freq='day', market=market, start=start_date)
#             if data is None or len(data) == 0:
#                 continue
#             data_num += len(data)
#             data_list.append(data)
#             if data_num > 2000:
#                 data = pd.concat(data_list)
#                 df_2_mysql(data, table_name)
#                 data_num = 0
#                 data_list.clear()
#
#     if data_num > 0:
#         data = pd.concat(data_list)
#         df_2_mysql(data, table_name)

@run_time
def save_stock_day(market='stock'):
    """
    从通达信获取交易日数据，并保存到mysql数据库中
    :param market: 市场类型，目前支持“stock/index/etf", 默认“stock".
    """
    cursor, conn = mysql_connect()
    try:
        stock_list = fetch_stock_list(market).index.to_list()
        end_date = now_time()[:10]
        table_name = market+'_day'
        max_date = mysql_to_df(cursor, f"SELECT code, MAX(date) as max_date FROM {table_name} GROUP BY code")
        if max_date is not None and len(max_date) > 0:
            max_date = max_date.set_index('code')

        cursor.execute(f"ALTER TABLE {table_name} DISABLE KEYS;")
        cursor.execute("SET UNIQUE_CHECKS=0;")
        cursor.execute("SET AUTOCOMMIT=0;")

        data_num = 0
        data_list = []
        for item in range(len(stock_list)):
            log.info('SAVE_{}_day : The {} of Total {}'.format(market, item, len(stock_list)))
            code = stock_list[item]
            if max_date is None or code not in max_date.index:
                start_date = '1991-01-01'
            else:
                start_date = str(max_date.loc[code, 'max_date'])[:10]

            if start_date != end_date:
                start_date = get_next_trade_day(start_date)
                log.info('Trying updating {} from {}'.format(code, start_date))
                data = fetch_price(code, freq='day', market=market, start=start_date)
                if data is None or len(data) == 0:
                    continue
                data_num += len(data)
                data_list.append(data)
                if data_num > 2000:
                    data = pd.concat(data_list)
                    df_to_mysql(cursor, data, table_name)
                    data_num = 0
                    data_list.clear()

        if data_num > 0:
            data = pd.concat(data_list)
            df_2_mysql(data, table_name)

        conn.commit()
    except Exception as e:
        conn.rollback()
        print('数据库操作错误:' + str(e))
    finally:
        cursor.execute(f"ALTER TABLE {table_name} ENABLE  KEYS;")
        cursor.execute("SET UNIQUE_CHECKS=1;")
        cursor.execute("SET AUTOCOMMIT=1;")
        cursor.close()
        conn.close()


# @run_time
# def save_stock_min(market='stock', freq='60min'):
#     """
#     从通达信获取交易分钟数据，并保存到mysql数据库中
#     :param market: 市场类型，目前支持“stock/index/etf", 默认“stock".
#     :param freq: 分钟频率，支持1min/5min/15min/30min/60min
#     """
#     if freq not in ["1min", "5min", "15min", "30min", "60min"] or\
#        market not in ["stock", "index", "etf"]:
#         log.error("save_stock_min: 输入参数错误！")
#
#     stock_list = fetch_stock_list(market).index.to_list()
#     end_date = now_time()[:10]
#     table_name = market+'_min'
#     max_date = mysql_2_df(f"SELECT code, MAX(datetime) as max_date FROM {table_name} WHERE type='{freq}' GROUP BY code")
#     if max_date is not None and len(max_date) > 0:
#         max_date = max_date.set_index('code')
#
#     data_num = 0
#     data_list = []
#     for item in range(len(stock_list)):
#         log.info('save_{}_min : The {} of Total {}'.format(market, item, len(stock_list)))
#         code = stock_list[item]
#         if max_date is None or code not in max_date.index:
#             start_date = '1991-01-01'
#         else:
#             start_date = str(max_date.loc[code, 'max_date'])[:10]
#
#         if start_date != end_date:
#             start_date = get_next_trade_day(start_date)
#             log.info('Trying updating {} from {}'.format(code, start_date))
#             data = fetch_price(code, freq=freq, market=market, start=start_date)
#             if data is None or len(data) == 0:
#                 continue
#             data['type'] = freq
#             data_num += len(data)
#             data_list.append(data)
#             if data_num > 2000:
#                 data = pd.concat(data_list)
#                 df_2_mysql(data, table_name)
#                 data_num = 0
#                 data_list.clear()
#
#     if data_num > 0:
#         data = pd.concat(data_list)
#         df_2_mysql(data, table_name)


@run_time
def save_stock_min(market='stock', freq='60min'):
    """
    从通达信获取交易分钟数据，并保存到mysql数据库中
    :param market: 市场类型，目前支持“stock/index/etf", 默认“stock".
    :param freq: 分钟频率，支持1min/5min/15min/30min/60min
    """
    if freq not in ["1min", "5min", "15min", "30min", "60min"] or\
       market not in ["stock", "index", "etf"]:
        log.error("save_stock_min: 输入参数错误！")

    cursor, conn = mysql_connect()
    try:
        stock_list = fetch_stock_list(market).index.to_list()
        end_date = now_time()[:10]
        table_name = market+'_min'
        max_date = mysql_to_df(cursor, f"SELECT code, MAX(datetime) as max_date FROM {table_name} WHERE type='{freq}' GROUP BY code")
        if max_date is not None and len(max_date) > 0:
            max_date = max_date.set_index('code')

        cursor.execute(f"ALTER TABLE {table_name} DISABLE KEYS;")
        cursor.execute("SET UNIQUE_CHECKS=0;")
        # cursor.execute("SET AUTOCOMMIT=0;")

        data_num = 0
        data_list = []
        for item in range(len(stock_list)):
            log.info('save_{}_min : The {} of Total {}'.format(market, item, len(stock_list)))
            code = stock_list[item]
            if max_date is None or code not in max_date.index:
                start_date = '1991-01-01'
            else:
                start_date = str(max_date.loc[code, 'max_date'])[:10]

            if start_date != end_date:
                start_date = get_next_trade_day(start_date)
                log.info('Trying updating {} from {}'.format(code, start_date))
                data = fetch_price(code, freq=freq, market=market, start=start_date)
                if data is None or len(data) == 0:
                    continue
                data['type'] = freq
                data_num += len(data)
                data_list.append(data)
                if data_num > 2000:
                    data = pd.concat(data_list)
                    df_to_mysql(cursor, data, table_name)
                    data_num = 0
                    data_list.clear()

        if data_num > 0:
            data = pd.concat(data_list)
            df_to_mysql(cursor, data, table_name)

        conn.commit()
    except Exception as e:
        conn.rollback()
        print('数据库操作错误:' + str(e))
    finally:
        cursor.execute(f"ALTER TABLE {table_name} ENABLE  KEYS;")
        cursor.execute("SET UNIQUE_CHECKS=1;")
        # cursor.execute("SET AUTOCOMMIT=1;")
        cursor.close()
        conn.close()


if __name__ == '__main__':
    # save_stock_min(market='index', freq='60min')
    # save_stock_day('stock')
    # save_stock_day('index')
    # save_stock_day('etf')
    # save_stock_list('stock')
    # save_stock_list('index')
    # save_stock_list('etf')
    for freq_ in ["1min", "5min", "15min", "30min", "60min"]:
        for market_ in ['stock', 'index', 'etf']:
            save_stock_min(market=market_, freq=freq_)
