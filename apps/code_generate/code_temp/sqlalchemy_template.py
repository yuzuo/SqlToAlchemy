# encoding:utf-8
__author__ = 'binpo'

from tornado import template

_get_do_name_temp = template.Template(u'''
class {{class_name}}(Base):
    """
    DAO class
    """
    __tablename__ = '{{table_name}}'
''')


_svr_header = template.Template(u"""# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------------
# DB API SERVICE generate from hslab tools
#
# @auth: xxxx@xxx.com
# ------------------------------------------------------------------------------------

import traceback

from base import BaseService
""")


_dao_header = template.Template(u"""# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------------
# DB API SERVICE generate from hslab tools
#
# @auth: xxxx@xxx.com
# ------------------------------------------------------------------------------------

import traceback

from sqlalchemy.sql.functions import now
from dao.base_dao import BaseDAO
""")

_model_header = template.Template(u"""# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------------
# DB API SERVICE generate from hslab tools
#
# @auth: xxxx@xxx.com
# ------------------------------------------------------------------------------------

import traceback

from model.base import Base
from sqlalchemy.sql.functions import now
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float
""")




_class_header = template.Template(u"""# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------------
# DB API SERVICE generate from hslab tools
#
# @auth: xxxx@xxx.com
# ------------------------------------------------------------------------------------

import traceback

from model.base import Base
from sqlalchemy.sql.functions import now
from dao.base_dao import BaseDAO
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float
""")


# -----------------------------------DAO-------------------------------------------
# 生成实体对象

get_dao_class_filed = template.Template(u"""
class {{class_name}}(BaseDAO):
    '''
    {{class_name}}实体对象
    '''
    def __init__(self, db):
        super({{class_name}}, self).__init__(db)
""")



# 根据参数获取对象实例
_get_do_by_params = template.Template(u'''
    def _get_{{table_name}}_by_params(self, **kwargs):
        """
        根据字典参数获取对象信息
        :param kwargs:
        :return:
        """
        query = self.db.query({{DO_NAME}})
        for key, val in kwargs.items():
            if hasattr({{DO_NAME}}, key):
                query = query.filter(getattr({{DO_NAME}}, key)==val)
        return query
''')

# 生成跟进对象id获取数据
_get_do_by_id = template.Template(u'''
    def _get_{{table_name}}_by_id(self, entry_id):
        """
        根据id获取数据
        :param kwargs:
        :return:
        """
        pars = {'id':str(entry_id)}
        return self._get_{{table_name}}_by_params(**pars).first()
''')


# 更新对象
_update_do_by_params = template.Template(u'''
    def _update_{{table_name}}_by_id(self, entry_id, **kwargs):
        """
        根据id 修改数据对象
        """
        entry = self._get_{{table_name}}_by_id(entry_id)
        if not entry:
            return False, 'item i is not exit', ''

        kwargs.update({'gmt_modified': now()})
        for k, v in kwargs.items():
            if hasattr(entry, k):
                setattr(entry, k, v)

        msg = '修改{}'
        if kwargs.get('deleted') == 1:
            entry.deleted = 1
            msg = '删除{}'
        else:
            entry.deleted = 0
        try:
            self.db.commit()
            return True, msg.format('成功'), entry
        except:
            self.db.rollback()
            self.log.error(traceback.format_exc())
            return False, msg.format('失败'), ''
''')


# 软删除对象
_delete_do_by_params = template.Template(u'''
    def _delete_item_by_id(self, entry_id):
        """
        根据id 删除数据对象
        """
        self.log.error('will delete {{table_name}} item %s' % entry_id)
        entry = self._get_{{table_name}}_by_id(entry_id)
        if not entry:
            return False,'item i is not exit',''

        entry.deleted = 1
        msg = '删除{}'
        try:
            self.db.commit()
            return True, msg.format('成功'), ''
        except:
            self.db.rollback()
            self.log.error(traceback.format_exc())
            return False, msg.format('失败'), ''
''')

# 新增对象
_add_do_by_params = template.Template(u'''
    def _add_item_by_params(self, **kwargs):
        """
        根据id修改数据对象
        """
        entry = {{entry}}
        for k, v in kwargs.items():
            if hasattr(entry, k):
                setattr(entry, k, v)
        return self._add_item_by_entry(entry)
''')


# 新增对象
_add_do_by_entry = template.Template(u'''
    def _add_item_by_entry(self, entry):
        """
        根据id修改数据对象
        @TODO  此处有缺陷，可以增加别的对象。 这样数据权限可能有问题。
        """
        msg = '新增{}'
        try:
            entry.gmt_created = now()
            entry.deleted = 0
            self.db.add(entry)
            self.db.commit()
            return True, msg.format('成功'), entry
        except:
            self.db.rollback()
            self.log.error(traceback.format_exc())
            return False, msg.format('失败'),''
''')





# -----------------------------------SERVICE-------------------------------------------
get_svr_class_field = template.Template(u"""
class {{class_name}}(BaseService):
    '''
    {{class_name}}实体对象
    '''
    def __init__(self, db):
        self.db = db
        self.{{table_name}}_dao = {{DAO_NAME}}(db)
""")


# 获取一条记录 -->id
_get_entry_service_by_id = template.Template(u'''
    def get_{{table_name}}_by_id(self, entry_id):
        """
        根据id获取数据
        :param kwargs:
        :return:
        """
        return self.{{table_name}}_dao._get_{{table_name}}_by_id(entry_id=entry_id)
''')

_get_entry_service_first = template.Template(u'''
    def get_{{table_name}}_first(self, **kwargs):
        """
        根据参数获取一条数据
        :param kwargs:
        :return:
        """
        return self.{{table_name}}_dao._get_{{table_name}}_by_params(**kwargs).first()
''')

_get_entry_service_list = template.Template(u'''
    def get_{{table_name}}_list(self, **kwargs):
        """
        根据参数获取数据列表
        :param kwargs:
        :return:
        """
        return self.{{table_name}}_dao._get_{{table_name}}_by_params(**kwargs).all()
''')


_add_service_by_params = template.Template(u'''
    def add_{{table_name}}(self, **kwargs):
        """
        添加数据
        :param kwargs:
        :return:
        """
        return self.{{table_name}}_dao._add_item_by_params(**kwargs)
''')

_update_service_by_params = template.Template(u'''
    def update_{{table_name}}_by_id(self, id, **kwargs):
        """
        根据id 修改数据对象
        :param kwargs:
        :return:
        """
        return self.{{table_name}}_dao._update_{{table_name}}_by_id(id,**kwargs)
''')

_delete_service_by_id = template.Template(u'''
    def delete_{{table_name}}_by_id(self, id):
        """
        根据id 删除数据对象
        """
        return self.{{table_name}}_dao._delete_item_by_id(id)
''')
