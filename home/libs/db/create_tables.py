#coding=utf-8
from dbsession import Base,engine

#创建所有引擎数据
def run():
    print '---------创建开始---------'
    Base.metadata.create_all(engine)
    print '---------创建结束---------'

if __name__ == '__main__':
    run()





