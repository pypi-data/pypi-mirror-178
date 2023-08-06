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
import pandas as pd
import pymysql
import contextlib
from pymysql.cursors import DictCursor

MAX_PACKET_ROWS = 5000

# MySql配置信息
HOST = os.getenv('MYSQL_HOST') or '192.168.0.14'
PORT = os.getenv('MYSQL_PORT') or 3306
DATABASE = os.getenv('MYSQL_DATABASE') or 'qff'
USERNAME = os.getenv('MYSQL_USERNAME') or 'root'
PASSWORD = os.getenv('MYSQL_PASSWORD') or '425415'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (USERNAME, PASSWORD, HOST, PORT, DATABASE)


# 定义上下文管理器，连接后自动关闭连接
@contextlib.contextmanager
def mysql():
    conn = pymysql.connect(host=HOST, port=int(PORT), user=USERNAME, password=PASSWORD, database=DATABASE,
                           charset='utf8mb4')
    cursor = conn.cursor(cursor=DictCursor)
    try:
        yield cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        print('数据库操作错误:'+str(e))
    finally:
        cursor.close()
        conn.close()


def df_2_mysql(data, table_name):
    with mysql() as cursor:
        data_len = len(data)
        start = 0
        while data_len > MAX_PACKET_ROWS:
            small_df = data.iloc[start:start+MAX_PACKET_ROWS]
            str_data = [tuple(x) for x in small_df.to_records(index=True)]
            sql = f"insert into {table_name} values " + str(str_data)[1:-1]
            cursor.execute(sql)
            start += MAX_PACKET_ROWS
            data_len -= MAX_PACKET_ROWS

        if data_len > 0:
            small_df = data.iloc[start:]
            str_data = [tuple(x) for x in small_df.to_records(index=True)]
            sql = f"insert into {table_name} values " + str(str_data)[1:-1]
            cursor.execute(sql)


def mysql_2_df(sql):
    with mysql() as cursor:
        ret = cursor.execute(sql)
        if ret > 0:
            return pd.DataFrame(cursor.fetchall())
        else:
            return None


def mysql_connect():
    conn = pymysql.connect(host=HOST, port=int(PORT), user=USERNAME, password=PASSWORD, database=DATABASE,
                           charset='utf8mb4')
    cursor = conn.cursor(cursor=DictCursor)
    return cursor, conn


def df_to_mysql(cursor, data, table_name):
    data_len = len(data)
    start = 0
    while data_len > MAX_PACKET_ROWS:
        small_df = data.iloc[start:start + MAX_PACKET_ROWS]
        str_data = [tuple(x) for x in small_df.to_records(index=True)]
        sql = f"insert into {table_name} values " + str(str_data)[1:-1]
        cursor.execute(sql)
        start += MAX_PACKET_ROWS
        data_len -= MAX_PACKET_ROWS

    if data_len > 0:
        small_df = data.iloc[start:]
        str_data = [tuple(x) for x in small_df.to_records(index=True)]
        sql = f"insert into {table_name} values " + str(str_data)[1:-1]
        cursor.execute(sql)


def mysql_to_df(cursor, sql):
    ret = cursor.execute(sql)
    if ret > 0:
        return pd.DataFrame(cursor.fetchall())
    else:
        return None


def is_exist_database():
    db = pymysql.connect(host=HOST, port=int(PORT), user=USERNAME, password=PASSWORD, charset='utf8mb4')
    cursor1 = db.cursor()
    sql = "select * from information_schema.SCHEMATA WHERE SCHEMA_NAME = '%s'  ; " % DATABASE
    res = cursor1.execute(sql)
    db.close()
    return res


def init_database():
    db = pymysql.connect(host=HOST, port=int(PORT), user=USERNAME, password=PASSWORD, charset='utf8mb4')
    cursor1 = db.cursor()
    sql = "CREATE DATABASE IF NOT EXISTS %s CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;" % DATABASE
    res = cursor1.execute(sql)
    db.close()
    return res