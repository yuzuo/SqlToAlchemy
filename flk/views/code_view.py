# -*- coding:utf-8 -*-
from flask import render_template, make_response, request
from flk.code_generate.mysql_for_sqlachemy import make_model_code, make_dao_code, make_service_code, make_code, \
    make_act_dir, write_act_file, make_init_file
from flk.common.geration_tool import get_tables_info, get_table_fileds
from flk.config import base_dir

__author__ = 'shenhai'
from flask import Blueprint

api = Blueprint('api', __name__)


@api.route('/', methods=['GET'])
def table_opts_home_handler():
    tables = get_tables_info()
    return render_template('opts/opts_home.html', tables=tables, currentTable=None)


@api.route('/opts/<tableName>', methods=['GET'])
def table_opts_handler(tableName, action=None):
    tables = get_tables_info()
    fields = get_table_fileds(tableName)
    data = {"tables": tables, "fields": fields, "currentTable": tableName}
    resp = render_template('opts/misc_data.html', **data)
    response = make_response(resp)
    if tableName:
        response.set_cookie('current_table', tableName)
    return response


@api.route('/ops/alchemy/<keymodel>')
def code_make_handler(keymodel):
    tables = get_tables_info()
    table_name = request.cookies.get("current_table")

    if table_name:
        if keymodel == "model":
            code = make_model_code(table_name)
        elif keymodel == "dao":
            code = make_dao_code(table_name)
        elif keymodel == "service":
            code = make_service_code(table_name)

    return render_template("opts/code_data.html", tables=tables, currentTable=table_name, code=code)


@api.route('/ops/package/<category>')
def code_to_package(category):
    tables = get_tables_info()
    for table in tables:
        if table:
            if category == "model":
                code = make_model_code(table)
            elif category == "dao":
                code = make_dao_code(table)
            elif category == "service":
                code = make_service_code(table)
            file_name = "%s_%s.py" % (table, category)
            my_dir = make_act_dir(base_dir, category)
            make_init_file(my_dir, category)
            write_act_file(my_dir, file_name, code)
    return 'make dir and file success'


@api.route('/ops/code/<code_type>')
def code_handler(code_type):
    if code_type == "sqlalchemy":
        tables = get_tables_info()
        table_name = request.cookies.get("current_table")
        code = "can not create code any more"
        if table_name:
            code = make_code(table_name)
        return render_template('opts/code_data.html', tables=tables, currentTable=table_name, code=code)
