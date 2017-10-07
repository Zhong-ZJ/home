#coding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 连接数据库的数据
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'rock_test'
USERNAME = 'rock1'
PASSWORD = 'rock1'

# DB_URI的格式：dialect（mysql/sqlite）+driver://username:password@host:port/database?charset=utf8
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)

# engine                                    		# engine引擎
engine = create_engine(DB_URI, echo=False )         # echo是否打印创建过程
Base = declarative_base(engine)                     # 创建基类


# sessionmaker生成一个session类
Session = sessionmaker(bind=engine)
dbSession = Session()                               # dbSession会话实例
