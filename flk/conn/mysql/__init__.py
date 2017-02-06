# -*- coding:utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import MySQLdb as mdb
from flk.config import mysql_user, mysql_pwd, mysql_host, mysql_db

engine = create_engine('mysql://%s:%s@%s/%s?charset=utf8' % (mysql_user, mysql_pwd, mysql_host, mysql_db),
                       convert_unicode=True, echo=False)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()





def get_cur():
    con = mdb.connect(mysql_host, mysql_user, mysql_pwd, mysql_db, connect_timeout=3, charset="utf8")
    with con:
        cur = con.cursor()
        return cur