# SqlToAlchemy
convert exist mysql table to sqlalchemy model
我比较懒，所以也懒得打包，懒得写requirements
需要:
tornado
sqlalchemy
MySQLdb




注意:这里我把tinyint直接转化成Boolean(sqlalchemy),但是其实如果tinyint>1,需要转化成Integer(sqlalchemy),自己定义tornado的mysql_conn