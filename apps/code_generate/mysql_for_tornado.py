# -*- coding: UTF-8 -*-
import StringIO

import MySQLdb as mdb
from setting import db_host, user_name, user_pwd, db_name


def get_cur():
    con = mdb.connect(db_host, user_name, user_pwd, db_name, connect_timeout=3)
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


#
# def get_table_fileds_info(table_name,code_type):
#     """
#     获取表所有字段
#     """
#     cur = get_cur()
#     cur.execute("SELECT * FROM %s" % table_name)
#     desc = cur.description
#     fileds = []
#     for i in xrange(0, len(desc)):
#         filed = desc[i][0]
#         filed_type = get_mysql_type(desc[i][1])
#         file_length = desc[i][3]
#         file_not_null = desc[i][-1]
#         info = (filed,filed_type,file_length,file_not_null)
#         fileds.append(info)
#     return fileds

# -------------------------------------------------------------------------------------------------------------


def get_all_file(table_name, code_type):
    """获取所有entry 对象
    """
    className = get_class_name(table_name)
    return eval(code_type).get_all_filed.generate(table_name=table_name, class_name=className)


def get_by_id(table_name, code_type):
    """根据id，获取entry 对象
    """

    class_name = get_class_name(table_name)
    return eval(code_type).get_by_id.generate(table_name=table_name, class_name=class_name)


def get_item_count(table_name, code_type):
    return eval(code_type).get_item_count.generate(table_name=table_name)


def delete_item(table_name, item_id, code_type):
    className = get_class_name(table_name)
    return eval(code_type).delete_item.generate(table_name=table_name, class_name=className, item_id=item_id)


def create_item(table_name, code_type):
    fileds = get_table_fileds(table_name)

    sql = ""
    values = ""
    parm = ""
    canshu = ""
    for filed in fileds:

        if filed == 'id':
            continue
        sql = sql + "'" + filed + "',"

        if filed == 'created' or filed == 'updated':
            values = values + "now(),"
        elif filed == 'deleted':
            values = values + "0,"
        else:
            values = values + "'%s',"
        parm = parm + filed + ","
        canshu = canshu + filed + ","

    sql = sql.rstrip(',')
    values = values.rstrip(',')
    parm = parm.rstrip(',')
    canshu = canshu.rstrip(',')
    className = get_class_name(table_name)
    return eval(code_type).create_item.generate(table_name=table_name, class_name=className, values=values, sql=sql,
                                                parm=parm, canshu=canshu, fileds=fileds)


def update_item(table_name, code_type):
    fileds = get_table_fileds(table_name)
    sql = ""
    values = ""
    parm = ""
    for filed in fileds:
        parm = parm + filed + ","
        if filed == 'id':
            continue

        if filed == 'created' or filed == 'updated':
            sql = sql + "t." + filed + "=now(),"
            values = values + "now(),"
        elif filed == 'deleted':
            values = values + "0,"
            sql = sql + "t." + filed + "=0,"
        else:
            values = values + filed + ","
            sql = sql + "t." + filed + "='%s',"

    sql = sql.rstrip(',')
    parm = parm.rstrip(',')
    values = values.rstrip(',')

    if not table_name:
        raise
    list = table_name.split('_')
    servie_name = ''
    for item in list:
        servie_name += item.capitalize()
    # servie_name += 'Service'
    return eval(code_type).update_item.generate(table_name=table_name, sql=sql, values=values, parm=parm, keys=fileds,
                                                className=servie_name)


def make_code(table_name="jlb_misc_data", item_id=100, code_type='torndb'):
    keys = {'tornado': 'p', 'sqlalchemy': 'o'}
    print '-------:', table_name

    classfile = create_class(table_name, keys.get(code_type, 'p'))
    allFiled = get_all_file(table_name, keys.get(code_type, 'p'))
    byid = get_by_id(table_name, keys.get(code_type, 'p'))
    itemCount = get_item_count(table_name, keys.get(code_type, 'p'))
    deleteItem = delete_item(table_name, item_id, keys.get(code_type, 'p'))
    createItem = create_item(table_name, keys.get(code_type, 'p'))
    updateItem = update_item(table_name, keys.get(code_type, 'p'))

    s = StringIO.StringIO()
    s.write(classfile)
    s.write((createItem))
    s.write(updateItem)
    s.write(deleteItem)
    s.write(allFiled)
    s.write(byid)
    s.write(itemCount)
    s.seek(0)
    tem = s.read()
    s.close()
    return tem


def make_sqlachemy_code(table_name="jlb_misc_data", item_id=100, code_type='torndb'):
    keys = {'tornado': 'p', 'sqlalchemy': 'o'}
    print '-------:', table_name

    classfile = create_class(table_name, keys.get(code_type, 'p'))
    allFiled = get_all_file(table_name, keys.get(code_type, 'p'))
    byid = get_by_id(table_name, keys.get(code_type, 'p'))
    itemCount = get_item_count(table_name, keys.get(code_type, 'p'))
    deleteItem = delete_item(table_name, item_id, keys.get(code_type, 'p'))
    createItem = create_item(table_name, keys.get(code_type, 'p'))
    updateItem = update_item(table_name, keys.get(code_type, 'p'))

    s = StringIO.StringIO()
    s.write(classfile)
    s.write((createItem))
    s.write(updateItem)
    s.write(deleteItem)
    s.write(allFiled)
    s.write(byid)
    s.write(itemCount)
    s.seek(0)
    tem = s.read()
    s.close()
    return tem


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
    type_map["BLOB"] = 252
    type_map["VAR_STRING"] = 253

    for k, v in type_map.items():
        if v == int(type):
            return k

    return "unknow type"


def create_class(table_name, code_type='tornadb'):
    if not table_name:
        raise
    list = table_name.split('_')
    servie_name = ''
    for item in list:
        servie_name += item.capitalize()
    servie_name += 'Service'

    return eval(code_type).get_class_filed.generate(className=servie_name)


def get_class_name(table_name):
    if not table_name:
        raise
    list = table_name.split('_')
    servie_name = ''
    for item in list:
        servie_name += item.capitalize()
    return servie_name


def get_service_name():
    return get_class_name() + "Service"


if __name__ == '__main__':
    table_name = "my_area"
    print make_code(table_name, item_id=10)
