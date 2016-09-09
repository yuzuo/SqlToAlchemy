# -*- coding: UTF-8 -*-
from tornado import template

__author__ = 'fangshi'

get_class_filed = template.Template( u"""
# -*- coding: UTF-8 -*-
#------------------------------------------------------------------------------------
# DB API SERVICE generate from hslab tools
#
# @auth: fangshi8080@126.com
#------------------------------------------------------------------------------------


class {{className}}(BaseService):
    '''
    generate from hslab tools
    '''
    def __init__(self, db):
        self.db = db
"""
)


get_all_filed = template.Template(u'''
    def get_all_filed(self, query=None):
        """
        获取{{table_name}}所有字段
        """
        if query:
            sql = "select * from {{table_name}} n where n.deleted=0 order by n.created desc limit %s, %s;"
            pars = (query.start_row, query.end_row)
            return self.db().query(sql, *pars)
        else:
            sql = "select * from {{table_name}} n where n.deleted=0 order by n.created desc limit %s, %s;"
            pars = (0, 12)
            return self.db().query(sql, *pars)
    '''
)


get_by_id = template.Template(u'''
    def get_by_id(self, item_id=0):
        """
        根据id查询
        """
        if item_id and item_id >= 0:
            sql = "select * from {{table_name}} n where n.id = %s"
            pars = (item_id)
            return self.db().get(sql,*pars)
    '''
)


get_item_count = template.Template(u'''
    def get_item_count(self):
        """
        返回item个数
        """
        sql = "select count(id) from {{table_name}};"
        return self.db().query(sql)
    '''
)


delete_item = template.Template(u'''
    def delete_item(self,item_id=0):
        """
        根据item_id删除item数据
        """
        if item_id and item_id >=0:
            sql = """update {{table_name}} t set t.deleted=1
            where t.id = %s and t.deleted=0;"""
            pars = (item_id)
            self.db().execute(sql, *pars)
    '''
)


create_item = template.Template(u'''
    def create_item(self, {{canshu}}):
        """
        insert into {{table_name}}
        """
        sql = """insert into {{table_name}}({{sql}}) values({{values}})
            """
        pars = ({{parm}})
        return self.db().execute_rowcount(sql, *pars)
    '''
)



update_item = template.Template(u'''
    def update_{{table_name}}(self, {{parm}}):
        """
        更新{{table_name}}
        """
        sql = u"""update {{table_name}} t set  {{sql}}
        where t.id = %s; """
        pars = ({{values}})
        self.db().execute(sql, *pars)
    '''
)


