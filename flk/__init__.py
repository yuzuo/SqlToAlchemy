# -*- coding:utf-8 -*-
from flask import Flask
from flk.conn.mysql import db_session
from flk.views.code_view import api

__author__ = 'shenhai'

app = Flask(__name__)


app.register_blueprint(api)
app.secret_key = "kxk031-3DSkslaldp2ajef!@3ksdfj"


@app.teardown_request
def shutdown_session(exception=None):
    print "mysql conn remove when request finish"
    db_session.remove()
