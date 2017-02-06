# -*- coding: UTF-8 -*-
from jinja2 import Template

__author__ = 'shs'


get_all_filed = Template(u'''
def get_all_filed(self, query=None):
    """
    获取{{table_name}}所有字段
    """
    if query:
        sql = "select * from {{table_name}} n where n.deleted=0 order by n.created desc limit %s, %s;" % (
        query.start_row, query.end_row)
        return self.db().query(sql)
    else:
        sql = "select * from {{table_name}} n where n.deleted=0 order by n.created desc limit %s, %s;" % (0, 12)
        return self.db().query(sql)
''')


get_by_id = Template(u'''
def get_by_id(self, item_id=0):
    """
    根据id查询
    """
    if item_id and item_id >= 0:
        sql = "select * from {{table_name}} n where n.id = %s" % int(item_id)
        return self.db().get(sql)
''')


get_item_count = Template(u'''
def get_item_count(self):
    """
    返回item个数
    """
    sql = "select count(id) from {{table_name}};"
    return self.db().query(sql)
''')


delete_item = Template(u'''
def delete_item(self,item_id=0):
    """
    根据item_id删除item数据
    """
    if item_id and item_id >=0:
        sql = """update {{table_name}} t set t.deleted=1
        where t.id = %s and t.deleted=0;""" % item_id
        self.db().execute(sql)
''')


create_item = Template(u'''
def create_item(self, {{canshu}}):
    """
    insert into {{table_name}}
    """
    sql = """insert into {{table_name}}({{sql}}) values({{values}}
        """ % ({{parm}})
    return self.db().execute_rowcount(sql)
''')



update_item = Template(u'''
def update_{{table_name}}(self, {{parm}}):
    """
    更新{{table_name}}
    """
    sql = u"""update {{table_name}} t set  {{sql}}
    where t.id = %s; """ % ({{values}})
    self.db().execute(sql)
''')


