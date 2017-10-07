#coding=utf-8
from datetime import datetime
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import define,options


from models.sql import Hous_area
from libs.db.dbsession import dbSession

from urls import handlers
from config import settings
from libs.db import create_tables




define('post',default=2000,type=int,help="home sever")
define('t',default=False,type=bool,help="carete table")
define('s',default=False,type=bool,help="carete table")



def create_h():
    dbSession.add_all([
        Hous_area(area_id=1,area_name='天河区',area_ctime=datetime.now()),
        Hous_area(area_id=2,area_name='荔湾区',area_ctime=datetime.now()),
        Hous_area(area_id=3,area_name='海珠区',area_ctime=datetime.now()),
        Hous_area(area_id=4,area_name='越秀区',area_ctime=datetime.now()),
        Hous_area(area_id=5,area_name='白云区',area_ctime=datetime.now()),
        Hous_area(area_id=6,area_name='黄埔区',area_ctime=datetime.now()),
        Hous_area(area_id=7,area_name='番禺区',area_ctime=datetime.now()),
        Hous_area(area_id=8,area_name='花都区',area_ctime=datetime.now()),
        Hous_area(area_id=9,area_name='南沙区',area_ctime=datetime.now()),
        Hous_area(area_id=10,area_name='增城区',area_ctime=datetime.now()),
        Hous_area(area_id=11,area_name='从化区',area_ctime=datetime.now()),
    ])
    dbSession.commit()






if __name__ == '__main__':
    # options.log_file_prefix = config.log_path
    # options.logging = config.log_level

    tornado.options.parse_command_line()
    if options.t:create_tables.run()

    if options.s:create_h()



    app = tornado.web.Application(handlers,**settings)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.post)
    tornado.ioloop.IOLoop.instance().start()













