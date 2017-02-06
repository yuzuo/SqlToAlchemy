# -*- coding:utf-8 -*-
from flask import render_template, make_response, request
from flk.code_generate.mysql_for_sqlachemy import make_model_code, make_dao_code, make_service_code, make_code
from flk.common.geration_tool import get_tables_info, get_table_fileds

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


@api.route('/ops/code/<code_type>')
def code_handler(code_type):
    if code_type == "sqlalchemy":
        tables = get_tables_info()
        table_name = request.cookies.get("current_table")
        code = "can not create code any more"
        if table_name:
            code = make_code(table_name)
        return render_template('opts/code_data.html', tables=tables, currentTable=table_name, code=code)
