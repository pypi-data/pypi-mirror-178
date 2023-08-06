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
从数据库中查询股票价格数据
"""

import pandas as pd
from datetime import datetime
from bson.regex import Regex
from qff.tools.config import DATABASE
from qff.tools.date import util_time_stamp, get_pre_trade_day, is_trade_day, get_real_trade_date, util_date_valid
from qff.tools.utils import util_code_tolist
from qff.tools.logs import log
from qff.frame.context import context


def get_price(security, start=None, end=None, freq='daily', fields=None, skip_paused=False, fq='pre', count=None,
              market='stock'):
    """
    获取历史数据，可查询一支或者多只股票的行情数据, 按天或者按分钟，返回数据格式为 DataFrame
    :param security: 一支股票代码或者一个股票代码的list
    :param count: 与 start 二选一，不可同时使用. 数量, 返回的结果集的行数, 即表示获取 end_date 之前几个
                   frequency 的数据
    :param start: 与 count 二选一，不可同时使用. 字符串或者 datetime.datetime/datetime.date 对象, 开始时间.
                    (1)如果 count 和 start_date 参数都没有, 则 start 生效, 等于 end. 注意:
                    (2)当取分钟数据时, 时间可以精确到分钟, 比如: 传入datetime.datetime(2015, 1, 1, 10, 0, 0)
                    或者 '2015-01-01 10:00:00'
                    (3)当取分钟数据时, 如果只传入日期, 则日内时间是当日的 00:00:00.
                    (4)当取天数据时, 传入的日内时间会被忽略

    :param end: 格式同上, 结束时间, 默认是当前日期的前一个交易日, 包含此日期. 注意: 当取分钟数据时, 如果 end 只有日期,
                则日内时间等同于 00:00:00, 所以返回的数据是不包括 end 这一天的.
    :param freq: 单位时间长度, 几天或者几分钟, 现在支持'Xd','Xm', 'daily'(等同于'1d'), 'minute'(等同于'1m'), X是
                 一个正整数, 分别表示X天和X分钟(不论是按天还是按分钟回测都能拿到这两种单位的数据)，默认值是daily
    :param fields: 字符串list, 选择要获取的行情数据字段, 默认是None(表示['open', 'close', 'high', 'low', 'vol',
                   'amount']这几个标准字段), 支持SecurityUnitData里面的所有基本属性，包含：['open', 'close', 'low',
                   'high','vol', 'amount', 'high_limit','low_limit', 'avg', 'pre_close', 'paused'],
                   其中paused为True表示停牌。
    :param skip_paused: 是否跳过不交易日期(包括停牌, 未上市或者退市后的日期). 如果不跳过, 停牌时会使用停牌前收盘价数据填充。
                    注意：本参数仅针对查询单个股票时有效。
    :param fq: 复权选项: 'pre', 前复权； None,不复权, 返回实际价格；'post',后复权，暂未实现

    :param market: 市场类型，目前支持“stock"和”index", 默认“stock".
    :return: 请注意, 为了方便比较一只股票的多个属性, 同时也满足对比多只股票的一个属性的需求, 我们在security参数是一只股票
             和多只股票时返回的结构完全不一样.
             .如果是一支股票, 则返回[pandas.DataFrame]对象, 行索引是date(分钟级别数据为datetime), 列索引是行情字段名字.
             .如果是多支股票, 则返回[pandas.DataFrame]对象,行索引是['date', 'code'],或['datetime', 'code']
    """
    log.debug('调用get_price'+str(locals()).replace('{', '(').replace('}', ')'))
    try:
        if market == 'stock':
            if freq in ['daily', '1d', 'day']:
                return get_stock_day_price(security, start, end, fields, skip_paused, fq, count)
            elif freq in ['1min', '5min', '15min', '30min', '60min', '1m', '5m', '15m', '30m', '60m']:
                return get_stock_min_price(security, start, end, freq, fields, skip_paused, fq, count)
            else:
                log.error('get_price：freq参数错误！')
                return None
        elif market == 'index':
            if freq in ['daily', '1d', 'day']:
                return get_index_day_price(security, start, end, fields, count)
            elif freq in ['1min', '5min', '15min', '30min', '60min', '1m', '5m', '15m', '30m', '60m']:
                return get_index_min_price(security, start, end, freq, fields, count)
            else:
                log.error('get_price：freq参数错误！')
                return None
        else:
            log.error('get_price：market参数错误！只能为stock和index')
            return None
    except Exception as e:
        log.error('get_price查询股票历史数据错误！:{}'.format(e))
        return None


def history(count, unit='1d', field='close', security_list=None, skip_paused=False, fq='pre'):
    """
    回测环境/模拟专用API
    获取历史数据，可查询多个股票的单个数据字段，返回数据格式为 DataFrame
    当取天数据时, 不包括当天的, 即使是在收盘后；分钟数据不包括当前分钟的数据，没有未来

    :param count: 数量, 返回的结果集的行数
    :param unit: 单位时间长度, 几天或者几分钟, 现在支持'1d','Xm', X是一个正整数, 分别表示X天和X分钟
    :param field:  要获取的数据类型,只能是一个值,包含：['open', ' close', 'low', 'high', 'vol', 'amount']
    :param security_list: 要获取数据的股票列表,None 表示查询 context.universe 中所有股票的数据
    :param skip_paused: 是否跳过不交易日期(包括停牌). 如果不跳过, 停牌时会使用停牌前的数据填充。
    :param fq: 复权选项。'pre'：前复权；'post':后复权；None:不复权
    :return:  [pandas.DataFrame]对象, 行索引是datetime字符串, 列索引是股票代号.

    """
    log.debug('调用history' + str(locals()).replace('{', '(').replace('}', ')'))
    code = security_list if security_list is not None else context.universe
    code = util_code_tolist(code)
    if unit == '1d':
        end_date = context.previous_date
        data = get_stock_day_price(code, end=end_date, fields=field, count=count, skip_paused=skip_paused, fq=fq)
        if data is not None:
            if len(code) > 1:
                data = data[field].reset_index().pivot(index='date', columns='code', values=field)
            else:
                data = data[field]

    elif unit in ['1m', '5m', '15m', '30m', '60m']:
        end_date = context.current_dt
        data = get_stock_min_price(code, end=end_date, freq=unit, fields=field, count=count + 1, fq=fq)
        if data is not None:
            if len(code) > 1:
                data = data[field].reset_index.pivot(index='datetime', columns='code', values=field)
            else:
                data = data[field]
            data = data.iloc[:-1]
    else:
        log.error("history():unit 参数错误!")
        return None

    return data


def attribute_history(security, count, unit='1d', fields=None, fq='pre'):
    """
    回测环境/模拟专用API
    查看某一支股票的历史数据, 可以选这只股票的多个属性, 默认跳过停牌日期.
    当取天数据时, 不包括当天的, 即使是在收盘后；分钟数据不包括当前分钟的数据，没有未来；

    :param security: 股票代码
    :param count: 数量, 返回的结果集的行数
    :param unit: 单位时间长度, 几天或者几分钟, 现在支持'1d','Xm', X是一个正整数, 分别表示X天和X分钟
    :param fields: 包含：['open', ' close', 'low', 'high', 'vol', 'amount']
    :param fq: 复权选项: pre-前复权 None-不复权 post-后复权
    :return: [pandas.DataFrame]对象, 行索引是datetime字符串, 列索引是属性名字..
    """
    log.debug('调用attribute_history' + str(locals()).replace('{', '(').replace('}', ')'))
    if fields is None:
        fields = ['open', 'close', 'high', 'low', 'vol', 'amount']
    if unit == '1d':
        end_date = context.previous_date
        data = get_stock_day_price(security, end=end_date, fields=fields, count=count, fq=fq)
        data = data[fields]

    elif unit in ['1m', '5m', '15m', '30m', '60m']:
        end_date = context.current_dt
        data = get_stock_min_price(security, end=end_date, freq=unit, fields=fields, count=count + 1, fq=fq)
        data = data[fields].iloc[:-1]
    else:
        log.error("attribute_history(): unit 参数错误!")
        return None
    return data


def get_stock_day_price(code, start=None, end=None, fields=None, skip_paused=False, fq='pre', count=None):
    """
    获取股票列表的日K线价格数据，直接访问本地数据库
    :param code: 一个单独的股票代码或者股票列表
    :param start: 开始日期时间字符串，与count二选一，如果同时存在，count参数无效
    :param end: {str:10 or str:19} --  结束日期时间字符串
    :param fields: 字符串list, 选择要获取的行情数据字段, 默认是None(表示['open', 'close', 'high', 'low', 'vol',
                   'amount']这几个标准字段),暂不支持 ['high_limit','low_limit', 'avg', 'pre_close', 'paused']
    :param skip_paused: 是否跳过不交易日期(包括停牌). 如果不跳过, 停牌时会使用停牌前的数据填充。
    :param fq: 复权选项。'pre'：前复权；'post':后复权（不支持）；None:不复权
    :param count: int数量, 返回的结果集的行数 TODO：当skip_paused为True时，返回的结果集行数会出现小于count值的情况
    :return: DataFrame数据类型, vol返回的成交股票数量（不是手）
    """
    if end is None:
        end = datetime.now().strftime('%Y-%m-%d')
        if not is_trade_day(end):
            end = get_real_trade_date(end)
    if start is None:
        if count is None:
            start = end
        else:
            start = get_pre_trade_day(end, count - 1)
    start = str(start)[0:10]
    end = str(end)[0:10]
    code = util_code_tolist(code)
    if fields is None:
        projection = {"_id": 0, "date_stamp": 0}
    else:
        if isinstance(fields, str):
            fields = [fields]
        if isinstance(fields, list):
            base_fields = [elem for elem in fields if elem in
                           ['open', 'close', 'low', 'high', 'vol', 'amount']]
            if len(base_fields) == 0:
                log.error("参数fields不合法！,应该为['open', 'close', 'low', 'high', 'vol', 'amount']列表！")

            if skip_paused and 'vol' not in base_fields:
                base_fields.append('vol')

            projection = dict.fromkeys(base_fields, 1)
            prefix = {
                "_id": 0,
                "code": 1,
                "date": 1,
            }
            projection = dict(**prefix, **projection)

        else:
            log.error("get_stock_day_price():参数fields不合法！,应该为字符串列表！")
            return None

    cursor = DATABASE.stock_day.find(
        {
            'code': {
                '$in': code
            },
            "date_stamp":
                {
                    "$lte": util_time_stamp(end),
                    "$gte": util_time_stamp(start)
                }
        },
        projection=projection,
        batch_size=10000
    )
    data = pd.DataFrame([item for item in cursor])
    try:
        data.drop_duplicates(['date', 'code'], inplace=True)
        if skip_paused:
            data = data.query('vol>1').copy()
            if fields and 'vol' not in fields:
                data = data.drop('vol', axis=1)
        data.set_index(['date', 'code'], inplace=True)
        if 'vol' in data.columns.values:
            data.vol = data.vol.apply(lambda x: int(x * 100))  # 股票成交数量不能有小数
        if 'amount' in data.columns.values:
            data.amount = data.amount.apply(lambda x: round(x, 2))  # 股票成交额保留两位小数

    except Exception as er:
        log.error("get_stock_day_price()获取股票日数据错误:{}".format(er))
        return None

    if fq == 'pre':
        cursor = DATABASE.stock_adj.find(
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
        adj = pd.DataFrame([item for item in cursor])
        try:
            adj.set_index(['date', 'code'], inplace=True)
            data = data.join(adj)

            for col in ['open', 'high', 'low', 'close']:
                if col in data.columns.values:
                    data[col] = round(data[col] * data['adj'], 2)

            data.drop('adj', axis=1, inplace=True)
        except Exception as er:
            log.error("get_stock_day_price()获取复权因子错误:{}".format(er))
            return data

    if len(code) == 1:
        data = data.reset_index().drop('code', axis=1).set_index("date")

    return data


def get_stock_min_price(code, start=None, end=None, freq='1m', fields=None, skip_paused=False, fq="pre", count=None):
    """
    获取股票列表分钟K线价格数据，直接访问本地数据库
    :param code: 一个单独的股票代码或者股票列表
    :param start: 开始日期时间字符串，与count二选一，如果同时存在，count参数无效
    :param end: {str:10 or str:19} 结束日期时间字符串
    :param freq: 字符串str 分钟线的类型 支持 1min 1m 5min 5m 15min 15m 30min 30m 60min 60m 类型
    :param fields: 字符串list, 选择要获取的行情数据字段, 默认是None(表示['open', 'close', 'high', 'low', 'vol',
               'amount']这几个标准字段)
    :param skip_paused: 是否跳过不交易日期(包括停牌). 如果不跳过, 停牌时会使用停牌前的数据填充。
    :param fq: 复权选项。'pre'：前复权；'post':后复权；None:不复权
    :param count: int数量, 返回的结果集的行数, 即表示获取 end_date 之前几个 frequency 的数据
    :return: dataframe类型数据
    """
    if end is None:
        end = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if not is_trade_day(end[0:10]):
            end = get_real_trade_date(end)
    if start is None:
        if count is None:
            start = end[0:10]
        else:
            start = get_pre_trade_day(end, count, freq)
    if len(start) == 10:
        start = '{} 09:30:00'.format(start)

    if len(end) == 10:
        end = '{} 15:00:00'.format(end)

    if freq in ['1min', '1m']:
        freq = '1min'
    elif freq in ['5min', '5m']:
        freq = '5min'
    elif freq in ['15min', '15m']:
        freq = '15min'
    elif freq in ['30min', '30m']:
        freq = '30min'
    elif freq in ['60min', '60m']:
        freq = '60min'
    else:
        log.error(
            "get_stock_min_price parameter freq=%s is none of 1min 1m 5min 5m 15min 15m 30min 30m 60min 60m"
            % freq
        )
        return None

    code = util_code_tolist(code)

    if fields is None:
        projection = {"_id": 0, "date_stamp": 0, "time_stamp": 0, "type": 0}
    else:
        if isinstance(fields, str):
            fields = [fields]
        if isinstance(fields, list):
            base_fields = [elem for elem in fields if elem in
                           ['open', 'close', 'low', 'high', 'vol', 'amount']]
            if len(base_fields) == 0:
                log.error("参数fields不合法！,应该为['open', 'close', 'low', 'high', 'vol', 'amount']列表！")

            if skip_paused and 'vol' not in base_fields:
                base_fields.append('vol')

            projection = dict.fromkeys(base_fields, 1)
            prefix = {
                "_id": 0,
                "code": 1,
                "date": 1,
                "datetime": 1,
            }
            projection = dict(**prefix, **projection)

        else:
            log.error("参数fields不合法！,应该为字符串列表！")
            return None

    cursor = DATABASE.stock_min.find(
        {
            'code': {
                '$in': code
            },
            "time_stamp":
                {
                    "$gte": util_time_stamp(start),
                    "$lte": util_time_stamp(end)
                },
            'type': freq
        },
        projection=projection,
        batch_size=10000
    )

    data = pd.DataFrame([item for item in cursor])
    try:

        data.drop_duplicates(['datetime', 'code'], inplace=True)
        if skip_paused:
            data = data.query('vol>1').copy()
            if fields and 'vol' not in fields:
                data = data.drop('vol', axis=1)
        if 'vol' in data.columns.values:
            data.vol = data.vol.apply(lambda x: int(x))  # 股票成交数量不能有小数
        if 'amount' in data.columns.values:
            data.amount = data.amount.apply(lambda x: round(x, 2))  # 股票成交额保留两位小数
        if count is not None:
            data = data.groupby(['code'], as_index=False).tail(count)
    except Exception as er:
        log.error("获取股票日数据错误:{}".format(er))
        return None

    if fq == 'pre':
        cursor = DATABASE.stock_adj.find(
            {
                'code': {
                    '$in': code
                },
                "date": {
                    "$lte": str(end)[0:10],
                    "$gte": str(start)[0:10]
                }
            },
            {"_id": 0},
            batch_size=10000
        )
        adj = pd.DataFrame([item for item in cursor])
        if len(adj) > 0:
            data.set_index(['date', 'code'], inplace=True, drop=False)
            adj.set_index(['date', 'code'], inplace=True)
            data = data.join(adj).set_index(['datetime', 'code'])
            for col in ['open', 'high', 'low', 'close']:
                if col in data.columns.values:
                    data[col] = round(data[col] * data['adj'], 2)
            data.drop(['date', 'adj'], axis=1, inplace=True)
            if len(code) == 1:
                data = data.reset_index().drop('code', axis=1).set_index("datetime")
            return data
        else:
            return data
    else:
        data.drop('date', axis=1, inplace=True)
        if len(code) == 1:
            data = data.drop('code', axis=1).set_index("datetime")
        else:
            data.set_index(['datetime', 'code'], inplace=True)
        return data


def get_index_day_price(code, start=None, end=None, fields=None, count=None):
    """
    获取指数列表的日K线价格数据，直接访问本地数据库
    :param code: 一个单独的指数代码或者列表
    :param start: 开始日期时间字符串，与count二选一，如果同时存在，count参数无效
    :param end: {str:10 or str:19} --  结束日期时间字符串
    :param fields: 字符串list, 选择要获取的行情数据字段, 默认是None(表示['open', 'close', 'high', 'low', 'vol',
                   'amount']这几个标准字段),另外支持 ['up_count','down_count']
    :param count: int数量, 返回的结果集的行数
    :return: DataFrame数据类型
    """
    if end is None:
        end = datetime.now().strftime('%Y-%m-%d')
        if not is_trade_day(end):
            end = get_real_trade_date(end)
    if start is None:
        if count is None:
            start = end
        else:
            start = get_pre_trade_day(end, count - 1)
    start = str(start)[0:10]
    end = str(end)[0:10]
    code = util_code_tolist(code)

    if fields is None:
        projection = {"_id": 0, "up_count": 0, "down_count": 0, "date_stamp": 0}
    else:
        if isinstance(fields, str):
            fields = [fields]
        if isinstance(fields, list):
            base_fields = [elem for elem in fields if elem in
                           ['open', 'close', 'low', 'high', 'vol', 'amount', 'up_count', 'down_count']]
            if len(base_fields) == 0:
                log.error("get_index_day_price()参数fields不合法！,应该为"
                          "['open', 'close', 'low', 'high', 'vol', 'amount', 'up_count', 'down_count']列表！")
            projection = dict.fromkeys(base_fields, 1)
            prefix = {
                "_id": 0,
                "code": 1,
                "date": 1,
            }
            projection = dict(**prefix, **projection)

        else:
            log.error("get_index_day_price()参数fields不合法！,应该为字符串列表！")
            return None

    cursor = DATABASE.index_day.find(
        {
            'code': {
                '$in': code
            },
            "date_stamp":
                {
                    "$lte": util_time_stamp(end),
                    "$gte": util_time_stamp(start)
                }
        },
        projection=projection,
        batch_size=10000
    )
    data = pd.DataFrame([item for item in cursor])
    try:
        data.drop_duplicates(['date', 'code'], inplace=True)
        if 'vol' in data.columns.values:
            data.vol = data.vol * 100
        if len(code) == 1:
            data = data.reset_index(drop=True).drop('code', axis=1).set_index("date")
        else:
            data.set_index(['date', 'code'], inplace=True)
        return data

    except Exception as err:
        log.error("get_index_day_price()获取指数日数据错误:{}".format(err))
        return None


def get_index_min_price(code, start=None, end=None, freq='1m', fields=None, count=None):
    """
    获取股票列表分钟K线价格数据，直接访问本地数据库
    :param code: 一个单独的股票代码或者股票列表
    :param start: 开始日期时间字符串，与count二选一，如果同时存在，count参数无效
    :param end: {str:10 or str:19} 结束日期时间字符串
    :param freq: 字符串str 分钟线的类型 支持 1min 1m 5min 5m 15min 15m 30min 30m 60min 60m 类型
    :param fields: 字符串list, 选择要获取的行情数据字段, 默认是None(表示['open', 'close', 'high', 'low', 'vol',
               'amount']这几个标准字段)
    :param count: int数量, 返回的结果集的行数, 即表示获取 end_date 之前几个 frequency 的数据
    :return: dataframe类型数据
    """
    if end is None:
        end = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if not is_trade_day(end[0:10]):
            end = get_real_trade_date(end)
    if start is None:
        if count is None:
            start = end[0:10]
        else:
            start = get_pre_trade_day(end, count, freq)
    if len(start) == 10:
        start = '{} 09:30:00'.format(start)

    if len(end) == 10:
        end = '{} 15:00:00'.format(end)

    if freq in ['1min', '1m']:
        freq = '1min'
    elif freq in ['5min', '5m']:
        freq = '5min'
    elif freq in ['15min', '15m']:
        freq = '15min'
    elif freq in ['30min', '30m']:
        freq = '30min'
    elif freq in ['60min', '60m']:
        freq = '60min'
    else:
        log.error(
            "get_index_min_price parameter freq=%s is none of 1min 1m 5min 5m 15min 15m 30min 30m 60min 60m"
            % freq
        )
        return None

    code = util_code_tolist(code)

    if fields is None:
        projection = {"_id": 0, "up_count": 0, "down_count": 0, "date": 0, "date_stamp": 0, "time_stamp": 0, "type": 0}
    else:
        if isinstance(fields, str):
            fields = [fields]
        if isinstance(fields, list):
            base_fields = [elem for elem in fields if elem in
                           ['open', 'close', 'low', 'high', 'vol', 'amount', 'up_count', 'down_count']]
            if len(base_fields) == 0:
                log.error("get_index_min_price()参数fields不合法！,应该为"
                          "['open', 'close', 'low', 'high', 'vol', 'amount', 'up_count', 'down_count']列表！")
            projection = dict.fromkeys(base_fields, 1)
            prefix = {
                "_id": 0,
                "code": 1,
                "datetime": 1,
            }
            projection = dict(**prefix, **projection)

        else:
            log.error("get_index_min_price()参数fields不合法！,应该为字符串列表！")
            return None

    cursor = DATABASE.index_min.find(
        {
            'code': {
                '$in': code
            },
            "time_stamp":
                {
                    "$gte": util_time_stamp(start),
                    "$lte": util_time_stamp(end)
                },
            'type': freq
        },
        projection=projection,
        batch_size=10000
    )

    data = pd.DataFrame([item for item in cursor])
    if len(data) == 0:
        log.warning("get_index_min_price未查询到数据")
        return None
    if count is not None:
        data = data.groupby(['code'], as_index=False).tail(count)
    data.drop_duplicates(['datetime', 'code'], inplace=True)

    if len(code) == 1:
        data = data.drop('code', axis=1).set_index("datetime")
    else:
        data.set_index(['datetime', 'code'], inplace=True)
    return data


def get_stock_list(date=None):
    """
    获取股票列表
    :param date: 在该日期上市的股票，如果为空，则取上一个交易日日期
    :return list: 返回股票代码列表
    """
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
        date = get_real_trade_date(date, -1)

    query_date = int(''.join(date.split('-')))
    collections = DATABASE.stock_info
    cursor = collections.find(
        {
            'ipo_date': {
                "$lte": query_date,
                "$gt": 0,
            }
        },
        {"_id": 0, "code": 1},
    )
    return [item["code"] for item in cursor]


def get_index_list():
    """ 获取指数列表 """
    collections = DATABASE.index_list
    cursor = collections.find(
        {},
        {"_id": 0, "code": 1},
    )
    return [item["code"] for item in cursor]


def get_index_stocks(index, date=None):
    """
    获取一个指数给定日期的成分股列表.目前仅支持
    '000016' ：上证50
    '000852' ：中证1000
    '000905' ：中证500
    '000906' ：中证800
    '000300' ：沪深300
    '000010' ：上证180
    '000688' ： 科创50

    :param index: 指数代码
    :param date: 查询日期, 一个字符串(格式类似'2015-10-15')
    :return: 返回股票代码的list
    """

    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
        date = get_real_trade_date(date, -1)

    coll = DATABASE.index_stock
    cursor = coll.find(
        {
            "index": index,
            "start": {"$lte": date},
            "end": {"$gte": date},
         },
        {"_id": 0, "code": 1},
    )
    return [item["code"] for item in cursor]


def get_stock_name(code=None, date=None):
    """
    获取股票名称
    :param code : 股票代码，支持list, 如果为空，则返回所有股票
    :param date : 查询日期，如果为空，则取上一个交易日日期
    :return dict: 返回股票代码与股票名称的字典
    """
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
        date = get_pre_trade_day(date)
    else:
        date = date[:10]

    collections = DATABASE.stock_name

    if code is not None:
        code = util_code_tolist(code)
        cursor = collections.find(
            {
                "date": date,
                "code": {
                    '$in': code
                },
            },
            {"_id": 0, "code": 1, "name": 1},
        )
    else:
        cursor = collections.find({"date": date}, {"_id": 0, "code": 1, "name": 1})
    return {item["code"]: item["name"] for item in cursor}


def get_index_name(code=None):
    """
    获取指数名称
    :param code : 指数代码，支持list, 如果为空，则返回所有指数
    :return dict: 返回股票代码与股票名称的字典
    """
    collections = DATABASE.index_list

    if code is not None:
        code = util_code_tolist(code)
        cursor = collections.find(
            {
                "code": {
                    '$in': code
                },
            },
            {"_id": 0, "code": 1, "name": 1},
        )
    else:
        cursor = collections.find({}, {"_id": 0, "code": 1, "name": 1})
    return {item["code"]: item["name"] for item in cursor}


def get_st_stock(code=None, date=None):
    """
    获取ST股票代码和名称
    :param code : 股票代码，支持list, 如果为空，则查询所有股票
    :param date : 查询日期，如果为空，则取最近交易日日期
    :return dict: 返回股票代码与股票名称的字典
    """
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
        # date = get_pre_trade_day(date)
        date = get_real_trade_date(date, -1)

    collections = DATABASE.stock_name
    if code is not None:
        code = util_code_tolist(code)
        cursor = collections.find(
            {
                "date": date,
                "code": {
                    '$in': code
                },
                "name": Regex(u".*ST.*", "i")
            },
            {"_id": 0, "code": 1, "name": 1},
        )
    else:
        cursor = collections.find(
            {
                "date": date,
                "name": Regex(u".*ST.*", "i")
            },
            {"_id": 0, "code": 1, "name": 1},
        )

    return {item["code"]: item["name"] for item in cursor}


def get_paused_stock(code=None, date=None):
    """
    获取停牌的股票代码
    :param code : 股票代码，支持list, 如果为空，则查询所有股票
    :param date : 查询日期，如果为空，则取最近交易日日期
    :return list: 返回股票代码列表
    """
    filter = {}
    if code is not None:
        if isinstance(code, str):
            code = [code]
        elif not isinstance(code, list):
            log.error("参数code不合法！,应该为字符串或列表！")
            return None
        filter['code'] = {'$in': code}

    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
        if not is_trade_day(date):
            date = get_real_trade_date(date)
    elif util_date_valid(date):
        if not is_trade_day(date):
            date = get_real_trade_date(date)
    else:
        log.error("参数date输入不合法！")
        return None

    filter['date_stamp'] = util_time_stamp(date)
    filter['vol'] = {'$lt': 1}

    coll = DATABASE.stock_day
    projection = {"_id": 0, "code": 1}
    cursor = coll.find(filter=filter, projection=projection)
    return [item["code"] for item in cursor]


def get_block_stock(block):
    """ 根据block名称检索对应的股票代码 """
    """
    blockname = 
    [
        300ESG,300周期,300非周,3D打印,5G概念,BIPV概念,C2M概念,CIPS概念,CXO概念,ETC概念
        HJT电池,IP变现,MCU芯片,MSCIA50,MSCI中盘,MSCI成份,MiniLED,NFT概念,NMN概念,OLED概念
        PPP模式,PVDF概念,QFII新进,QFII重仓,RCS概念,ST板块,一带一路,三代半导,上海自贸,上证180
        上证380,上证50,上证中盘,上证创新,上证治理,上证混改,上证红利,上证超大,不活跃股,专精特新
        业绩预升,业绩预增,业绩预降,东数西算,两年新股,个人持股,中俄贸易,中创100,中华A80,中字头
        中小100,中小300,中小银行,中盘价值,中盘成长,中证100,中证200,中证央企,中证红利,中证龙头
        久不分红,乡村振兴,亏损股,云游戏,云科技,云计算,互联金融,人工智能,人脑工程,人造肉
        代糖概念,仿制药,低价股,低市净率,低市盈率,体育概念,保险新进,保险重仓,信创,信息安全
        信托重仓,债转股,储能,元宇宙,充电桩,光伏,光刻机,免疫治疗,免税概念,养老概念
        养老金,内地低碳,军民融合,农业50,农村金融,冷链物流,分拆上市,分散染料,创业300,创业创新
        创业大盘,创业板50,创业板指,创业蓝筹,创医药,创成长,创投概念,创新100,创科技,创质量
        券商重仓,券商金股,化肥,北上重仓,北交所,北京冬奥,区块链,区块链50,医废处理,医美概念
        半导体50,博彩概念,卫星导航,即将解禁,参股新股,参股金融,双创50,发可转债,口罩防护,可燃冰
        台资背景,含B股,含GDR,含H股,含可转债,员工持股,商誉减值,回购计划,固态电池,国产软件
        国信价值,国开持股,国证价值,国证农业,国证基建,国证大宗,国证成长,国证服务,国证治理,国证红利
        国证芯片,国资云,国防军工,土地流转,在线消费,地下管网,地摊经济,地热能,垃圾分类,培育钻石
        基因概念,基金减仓,基金增仓,基金独门,基金重仓,壳资源,外资背景,大数据,大盘价值,大盘成长
        大盘股,大飞机,天然气,央企100,央企改革,央视50,婴童概念,字节跳动,安防服务,定增股
        定增预案,家庭医生,密集调研,富时A50,小盘价值,小盘成长,小米概念,工业互联,工业大麻,工业母机
        工业气体,已高送转,幽门菌,微利股,微盘股,恒大概念,成渝特区,户数减少,户数增加,扣非亏损
        投资时钟,抗癌,拟减持,拟增持,持续增长,换电概念,摘帽,操作系统,数字孪生,数字货币
        数据中心,整体上市,新冠检测,新冠药,新型烟草,新材料,新硬件,新能源车,新进成份,新零售
        无人机,无人驾驶,无线耳机,昨成交20,昨收活跃,昨日上榜,昨日振荡,昨日涨停,昨日跌停,昨日较弱
        昨日较强,昨日连板,昨日首板,昨曾涨停,昨曾跌停,昨高换手,智慧城市,智慧政务,智能交通,智能医疗
        智能家居,智能机器,智能电网,智能电视,智能穿戴,最近复牌,最近多板,最近异动,最近闪拉,最近闪跌
        有机硅,机构吸筹,板块趋势,核污防治,核电核能,次新开板,次新股,次新超跌,次新预增,武汉规划
        民企100,民营医院,民营银行,氟概念,氢能源,氮化镓,水产品,水利建设,污水处理,汽车拆解
        汽车电子,汽车芯片,沪深300,油气改革,泛珠三角,活跃股,海南自贸,海外业务,海峡西岸,消费100
        消费电子,涉矿概念,深次新股,深注册制,深证100,深证300,深证价值,深证创新,深证成指,深证成长
        深证治理,深证红利,烟草概念,燃料电池,物业管理,物联网,特斯拉,特高压,猪肉,环保50
        环渤海,生物疫苗,生物质能,电商概念,电子纸,电子身份,电解液,白酒概念,百元股,百度概念
        皖江区域,盐湖提锂,知识产权,石墨烯,破净资产,破发行价,碳中和,碳纤维,磷概念,社保新进
        社保重仓,种业,科创50,科创信息,科技100,租购同权,稀土永磁,稀缺资源,空气治理,粤港澳
        精选指数,绩优股,维生素,绿色建筑,绿色照明,绿色电力,网红经济,网络游戏,职业教育,聚氨酯
        股东减持,股东增持,股权分散,股权激励,股权转让,股权集中,胎压监测,能源互联,腾讯概念,腾讯济安
        航运概念,节能,芯片,苹果概念,草甘膦,虚拟现实,虫害防治,融资增加,融资融券,行业龙头
        被举牌,装配建筑,装饰园林,要约收购,证金汇金,资源优势,赛马概念,超导概念,超清视频,超级电容
        跨境电商,轮动趋势,辅助生殖,边缘计算,近已解禁,近期弱势,近期强势,近期新低,近期新高,远程办公
        连续亏损,送转潜力,送转超跌,透明工厂,通达信88,配股股,配股预案,重组股,重组预案,量子科技
        金融科技,钛金属,钠电池,钴金属,铁路基建,银河99,锂电池,锂矿,镍金属,长三角
        长株潭,阿里概念,陆股通减,陆股通增,降解塑料,雄安新区,页岩气,预制菜,预计扭亏,预计转亏
        预高送转,风沙治理,风能,风险提示,食品安全,高商誉,高市净率,高市盈率,高校背景,高端装备
        "高股息股","高融资盘","高贝塔值","高负债率","高质押股","鸡肉","鸿蒙概念","黄金概念"
    ]
    """
    collections = DATABASE.stock_block
    cursor = collections.find(
        {"blockname": block, "type": 'zs'},
        {"_id": 0, "code": 1},
    )
    return [item["code"] for item in cursor]


def get_stock_block(code):
    """ 根据股票代码检索对应的block名称 """
    collections = DATABASE.stock_block
    cursor = collections.find(
        {"code": code},
        {"_id": 0, "blockname": 1},
    )
    return [item["blockname"] for item in cursor]


def get_mtss(security_list, start_date, end_date, fields=None):
    """
    获取股票的融资融券信息
    获取一只或者多只股票在一个时间段内的融资融券信息
    :param security_list: 一只股票代码或者一个股票代码的 list
    :param start_date: 开始日期, 一个字符串
    :param end_date: 结束日期, 一个字符串
    :param fields: 字段名或者 list, 可选. 默认为 None, 表示取全部字段, 各字段含义如下：
    ____________________________________________
    段名	                  含义
    ____________________________________________
    date	              日期
    sec_code	          股票代码
    fin_value	          融资余额(元）
    fin_buy_value     	  融资买入额（元）
    fin_refund_value	  融资偿还额（元）
    sec_value	          融券余量（股）
    sec_sell_value	      融券卖出量（股）
    sec_refund_value	  融券偿还股（股）
    ____________________________________________

    :return: 返回一个 pandas.DataFrame 对象，默认的列索引为取得的全部字段. 如果给定了 fields 参数,
     则列索引与给定的 fields 对应.
    """
    if start_date is None:
        start_date = '2010-03-31'
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    if isinstance(security_list, str):
        security_list = [security_list]
    filter = {
        'code': {
            '$in': security_list
        },
        'date': {
            '$gte': start_date,
            '$lte': end_date
        }
    }
    if fields is None:
        projection = {'_id': 0}
    elif isinstance(fields, list):
        projection = dict.fromkeys(fields, 1)
        prefix = {
            "_id": 0,
            "code": 1,
            "date": 1
        }
        projection = dict(**prefix, **projection)
    else:
        projection = None

    cursor = DATABASE.stock_mtss.find(filter, projection)
    return pd.DataFrame([item for item in cursor])
