# -*- coding:utf-8 -*-
from tornado.web import RequestHandler

from tor.apps.code_generate import mysql_for_sqlachemy as s
from tor.apps.common.geration_tool import get_tables_info, get_table_fileds

__author__ = 'shihs'


class BaseHandler(RequestHandler):
    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('404.html')
        elif status_code == 500:
            self.render('500.html')
        else:
            super(RequestHandler, self).write_error(status_code, **kwargs)

    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        if not user_id:
            return None
        return self.db.get("SELECT * FROM user WHERE id = %s", int(user_id))


class TableOPTSHomeHandler(BaseHandler):
    """
        opts home
    """

    def get(self):
        tables = t.get_tables_info()
        self.render("opts/opts_home.html", tables=tables, currentTable=None)


class TableOPTSHandler(BaseHandler):
    """

    """

    def get(self, tableName, action=None):
        tables = get_tables_info()
        fileds = get_table_fileds(tableName)
        code = "can't create code any more"
        if tableName:
            self.set_cookie(name="current_table", value=tableName, expires_days=30)
        self.render("opts/misc_data.html", tables=tables, fileds=fileds, currentTable=tableName)



class CodeMakeHandler(BaseHandler):
    def get(self, key):
        tables = get_tables_info()
        table_name = self.get_cookie(name="current_table")
        code = ""
        if table_name:

            if key =="model":
                code = s.make_model_code(table_name)
            elif key=="dao":
                code = s.make_dao_code(table_name)
            elif key == "service":
                code = s.make_service_code(table_name)
        return self.render("opts/code_data.html", tables=tables, currentTable=table_name, code=code)





class CodeHandler(BaseHandler):
    """

    """

    def get(self, code_type='tornadb'):

        # if code_type == "tornadb":
        #     tables = t.get_tables_info()
        #     code = "can't create code any more"
        #     table_name = self.get_cookie(name="current_table")
        #     if table_name:
        #         code = make_code(table_name, code_type=code_type)
        #     self.render("opts/code_data.html", tables=tables, currentTable=table_name, code=code)

        if code_type == "sqlalchemy":
            tables = get_tables_info()
            code = "can't create code any more"
            table_name = self.get_cookie(name="current_table")
            if table_name:
                code = s.make_code(table_name)
            self.render("opts/code_data.html", tables=tables, currentTable=table_name, code=code)
