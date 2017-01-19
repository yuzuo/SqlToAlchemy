# -*- coding:utf-8 -*-
import re

import MySQLdb as mdb

from tor.settings import db_host, user_name, user_pwd, db_name

__author__ = 'liubo'


def get_do_name(table_name=None):
    return get_class_name(table_name) + "Do"


def get_dao_name(table_name=None):
    return get_class_name(table_name) + "Dao"


# -------------------------------------------Svr---------------------------------------------------------
def get_service_name(table_name=None):
    return get_class_name(table_name) + "Service"


def get_cur():
    con = mdb.connect(db_host, user_name, user_pwd, db_name, connect_timeout=3, charset="utf8")
    with con:
        cur = con.cursor()
        return cur


def get_tables_info():
    try:
        cur = get_cur()
        cur.execute("SHOW TABLES")
        result = cur.fetchall()
        tables = []
        for res in result:
            if res:
                tables.append(res[0])
        return tables
    except:
        raise


def get_table_fileds(table_name, code_type=None):
    """
    获取表所有字段
    """
    cur = get_cur()
    cur.execute("SELECT * FROM %s LIMIT 10" % table_name)
    desc = cur.description
    fileds = []
    for i in xrange(0, len(desc)):
        filed = desc[i][0]
        fileds.append(filed)
    return fileds


def get_table_fileds_info(table_name, code_type=None):
    """
    获取表所有字段
    """
    cur = get_cur()
    cur.execute("SHOW FULL COLUMNS FROM %s" % table_name)
    info = cur.fetchall()

    fields = []

    for field, type, collation, is_null, key, default, extra, privileges, comment in info:
        pattern = "(\w+)\((\d+)\)"
        if re.search(pattern, type):
            column_type, column_len = re.search(pattern, type).groups(0)
        else:
            column_type, column_len = type, None
        fields.append((field, column_type, is_null, key, default, comment, column_len))
    return fields


def get_mysql_type(type):
    if not type:
        return "unknow type"
    type_map = {}
    type_map["DECIMAL"] = 0
    type_map["TINY"] = 1
    type_map["SHORT"] = 2
    type_map["LONG"] = 3
    type_map["FLOAT"] = 4
    type_map["DOUBLE"] = 5
    type_map["NULL"] = 6
    type_map["TIMESTAMP"] = 7
    type_map["LONGLONG"] = 8
    type_map["INT24"] = 9
    type_map["DATE"] = 10
    type_map["TIME"] = 11
    type_map["DATETIME"] = 12
    type_map["YEAR"] = 13
    type_map["NEWDATE"] = 14
    type_map["VARCHAR"] = 15
    type_map["BIT"] = 16
    type_map["NEWDECIMAL"] = 246
    type_map["ENUM"] = 247
    type_map["SET"] = 248
    type_map["TINY_BLOB"] = 249
    type_map["MEDIUM_BLOB"] = 250
    type_map["LONG_BLOB"] = 251
    type_map["TEXT"] = 252
    type_map["VAR_STRING"] = 253

    for k, v in type_map.items():
        if v == int(type):
            return k

    return "unknow type"


def get_class_name(table_name):
    if not table_name:
        raise
    list = table_name.split('_')
    servie_name = ''
    for item in list:
        servie_name += item.capitalize()
    return servie_name
