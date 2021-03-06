# -*- coding: UTF-8 -*-
import StringIO
import codecs

from tor.apps.code_generate.code_temp import sqlalchemy_template as p
from tor.apps.common.geration_tool import get_tables_info, get_table_fileds_info, get_do_name, get_service_name, \
    get_dao_name


def get_is_null(is_null):
    if is_null == "NO":
        return " nullable = False, "
    else:
        return ""


def get_index(key):
    if key == "PRI":
        return " primary_key=True, "
    if key == "UNQ":
        return " unique = True, "

    if key == "MUL":
        return " index = True, "

    return ""


def get_default(default):
    if default != None:
        return " default = %s, " % (default)
    else:
        return ""


def make_do_code(table_name):
    type_map = {
        'int': 'Integer',
        'long': 'Integer',
        'varchar': 'String',
        'datetime': 'DateTime',
        'tinyint': 'Boolean',
        'float': 'Float',
        'text': 'Text'
    }

    str_class = StringIO.StringIO()

    get_tables_info()

    class_temp = p._get_do_name_temp.generate(class_name=get_do_name(table_name), table_name=table_name)
    str_class.writelines(class_temp)
    items = get_table_fileds_info(table_name)

    for field, column_type, is_null, key, default, comment, column_len in items:
        # temp = "%s = Column(%s%s)"
        for type_item in type_map.keys():
            if column_type == type_item:
                if field in ('gmt_created', 'gmt_modified') and column_type == 'datetime':
                    s = "    %s = Column(%s, %s %s %s doc='%s')\n" % (
                        field, type_map.get(type_item), get_index(key), get_is_null(is_null), "default=now(),",
                        comment)


                elif column_len != None and column_type != 'tinyint' and column_type != 'int':
                    s = "    %s = Column(%s(%s), %s %s %s doc='%s')\n" % (
                        field, type_map.get(type_item), column_len, get_index(key), get_is_null(is_null),
                        get_default(default), comment)

                else:
                    s = "    %s = Column(%s, %s %s %s doc='%s')\n" % (
                        field, type_map.get(type_item), get_index(key), get_is_null(is_null), get_default(default),
                        comment)

                str_class.writelines(s)
    str_class.write('\n')

    str_class.seek(0)
    s = str_class.read()
    str_class.close()
    return s



def make_svr_class_field(table_name=None):
    """

    :param table_name:
    :return:
    """
    svr_name = get_service_name(table_name)
    DAO_NAME = get_dao_name(table_name)
    class_temp = p.get_svr_class_field.generate(class_name=svr_name, table_name=table_name, DAO_NAME=DAO_NAME)
    return class_temp


def make_get_svr_by_id(table_name):
    return p._get_entry_service_by_id.generate(table_name=table_name)


def make_get_svr_by_params(table_name):
    return p._get_entry_service_first.generate(table_name=table_name)


def make_get_svr_list_by_params(table_name):
    return p._get_entry_service_list.generate(table_name=table_name)


def make_add_svr_by_params(table_name):
    return p._add_service_by_params.generate(table_name=table_name)


def make_update_svr_by_id(table_name):
    return p._update_service_by_params.generate(table_name=table_name)


def make_del_svr_by_id(table_name):
    return p._delete_service_by_id.generate(table_name=table_name)


# -------------------------------------------DAO---------------------------------------------------------

def make_dao_class_filed(table_name=None):
    dao_name = get_dao_name(table_name)
    class_temp = p.get_dao_class_filed.generate(class_name=dao_name)
    return class_temp


def make_get_do_by_params(table_name):
    query = '''
        # self.db.query(%s)
        for k,v in kwargs.items():
            if hasattr(%s, k):
                query.filter(getattr(%s, key)==val)
        return query
    '''
    DO_NAME = get_do_name(table_name)
    return p._get_do_by_params.generate(DO_NAME=DO_NAME, query=query, table_name=table_name)


def make_get_entry_by_id(table_name):
    """
    获取用户列表
    :param kwargs:
    :return:
    """
    return p._get_do_by_id.generate(table_name=table_name)


def make_update_do_by_params(table_name):
    """
    更新对象
    :param do_id
    :param kwargs:
    :return:
    """
    query = '''
        for k,v in kwargs.items():
            if hasattr(%s, k):
                entry.setattr(entry,k,v)
    '''
    return p._update_do_by_params.generate(query=query, table_name=table_name)


def make_delete_do_by_params(table_name):
    """
    删除数据对象
    """
    query = '''
        for k,v in kwargs.items():
            if hasattr(%s, k):
                entry.setattr(entry,k,v)
    '''
    return p._delete_do_by_params.generate(query=query, table_name=table_name)


def make_add_do_by_params(table_name):
    """
    新增对象数据
    """
    dao_name = get_do_name(table_name)

    entry = dao_name + '()'
    query = '''
        for k, v in kwargs.items():
            if hasattr(%s, k):
                entry.setattr(entry,k,v)
    '''
    return p._add_do_by_params.generate(entry=entry, query=query, table_name=table_name)


def make_add_do_by_entry(table_name):
    """
    新增对象数据
    """
    return p._add_do_by_entry.generate(table_name=table_name)


def make_model_code(table_name=None):
    if not table_name:
        return "table_name cant not be none"

    buffer = StringIO.StringIO()

    codecinfo = codecs.lookup("utf8")
    s = codecs.StreamReaderWriter(buffer,
                                  codecinfo.streamreader, codecinfo.streamwriter)

    header = p._model_header.generate()
    do_code = make_do_code(table_name)
    s.writelines(header)
    s.writelines(do_code)

    s.seek(0)
    tem = s.read()
    s.close()
    print tem
    return tem


def make_dao_code(table_name=None):
    """
    dao服务
    :param table_name:
    :return:
    """
    if not table_name:
        return "table_name cant not be none"

    buffer = StringIO.StringIO()

    codecinfo = codecs.lookup("utf8")
    s = codecs.StreamReaderWriter(buffer,
                                  codecinfo.streamreader, codecinfo.streamwriter)

    header = p._dao_header.generate()
    dao_code = make_dao_class_filed(table_name=table_name)
    bay_parms = make_get_do_by_params(table_name)
    by_id = make_get_entry_by_id(table_name)
    add_entry = make_add_do_by_entry(table_name)
    add_parems = make_add_do_by_params(table_name)
    update_by_parms = make_update_do_by_params(table_name)
    delete_item = make_delete_do_by_params(table_name)

    # ------ebd svr---
    s.writelines(header)
    s.writelines(dao_code.decode('utf8'))
    s.writelines(bay_parms.decode('utf8'))
    s.writelines(by_id.decode('utf8'))
    s.writelines(add_entry.decode('utf8'))
    s.writelines(add_parems.decode('utf8'))
    s.writelines(update_by_parms.decode('utf8'))
    s.writelines(delete_item.decode('utf8'))

    s.seek(0)
    tem = s.read()
    s.close()
    print tem
    return tem


def make_code(table_name=None):
    if not table_name:
        return "table_name cant not be none"

    buffer = StringIO.StringIO()

    codecinfo = codecs.lookup("utf8")
    s = codecs.StreamReaderWriter(buffer,
                                  codecinfo.streamreader, codecinfo.streamwriter)

    header = p._class_header.generate()
    do_code = make_do_code(table_name)
    dao_code = make_dao_class_filed(table_name=table_name)
    bay_parms = make_get_do_by_params(table_name)
    by_id = make_get_entry_by_id(table_name)
    add_entry = make_add_do_by_entry(table_name)
    add_parems = make_add_do_by_params(table_name)
    update_by_parms = make_update_do_by_params(table_name)
    delete_item = make_delete_do_by_params(table_name)
    # svr
    svr_code = make_svr_class_field(table_name=table_name)
    svr_id = make_get_svr_by_id(table_name=table_name)
    svr_first = make_get_svr_by_params(table_name=table_name)
    svr_list = make_get_svr_list_by_params(table_name=table_name)
    svr_add = make_add_svr_by_params(table_name=table_name)
    svr_del = make_del_svr_by_id(table_name=table_name)
    svr_edit = make_update_svr_by_id(table_name=table_name)
    # ------ebd svr---
    s.writelines(header)
    s.writelines(do_code)
    s.writelines(dao_code.decode('utf8'))
    s.writelines(bay_parms.decode('utf8'))
    s.writelines(by_id.decode('utf8'))
    s.writelines(add_entry.decode('utf8'))
    s.writelines(add_parems.decode('utf8'))
    s.writelines(update_by_parms.decode('utf8'))
    s.writelines(delete_item.decode('utf8'))
    # svr
    s.writelines(svr_code.decode('utf8'))
    s.writelines(svr_id.decode('utf8'))
    s.writelines(svr_first.decode('utf8'))
    s.writelines(svr_list.decode('utf8'))
    s.writelines(svr_add.decode('utf8'))
    s.writelines(svr_del.decode('utf8'))
    s.writelines(svr_edit.decode('utf8'))

    s.seek(0)
    tem = s.read()
    s.close()
    print tem
    return tem


def make_service_code(table_name=None):
    if not table_name:
        return "table_name cant not be none"

    buffer = StringIO.StringIO()

    codecinfo = codecs.lookup("utf8")
    s = codecs.StreamReaderWriter(buffer,
                                  codecinfo.streamreader, codecinfo.streamwriter)

    header = p._svr_header.generate()


    # svr
    svr_code = make_svr_class_field(table_name=table_name)
    svr_id = make_get_svr_by_id(table_name=table_name)
    svr_first = make_get_svr_by_params(table_name=table_name)
    svr_list = make_get_svr_list_by_params(table_name=table_name)
    svr_add = make_add_svr_by_params(table_name=table_name)
    svr_del = make_del_svr_by_id(table_name=table_name)
    svr_edit = make_update_svr_by_id(table_name=table_name)
    # ------ebd svr---
    s.writelines(header)

    # svr
    s.writelines(svr_code.decode('utf8'))
    s.writelines(svr_id.decode('utf8'))
    s.writelines(svr_first.decode('utf8'))
    s.writelines(svr_list.decode('utf8'))
    s.writelines(svr_add.decode('utf8'))
    s.writelines(svr_del.decode('utf8'))
    s.writelines(svr_edit.decode('utf8'))

    s.seek(0)
    tem = s.read()
    s.close()
    print tem
    return tem


if __name__ == '__main__':
    table_name = "my_active_base"
    make_code(table_name)
