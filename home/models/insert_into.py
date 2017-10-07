#coding=utf-8
from sql import Hous_area,Facility
from datetime import datetime
from libs.db.dbsession import dbSession

define('s',default=False,type=bool,help="carete table")

def create_h():
    dbSession.add_all([
        Hous_area(area_id=1,area_name='越秀区',area_ctime=datetime.now()),
        Hous_area(area_id=2,area_name='荔湾区',area_ctime=datetime.now()),
        Hous_area(area_id=3,area_name='海珠区',area_ctime=datetime.now()),
        Hous_area(area_id=4,area_name='天河区',area_ctime=datetime.now()),
        Hous_area(area_id=5,area_name='白云区',area_ctime=datetime.now()),
        Hous_area(area_id=6,area_name='黄埔区',area_ctime=datetime.now()),
        Hous_area(area_id=7,area_name='番禺区',area_ctime=datetime.now()),
        Hous_area(area_id=8,area_name='花都区',area_ctime=datetime.now()),
        Hous_area(area_id=9,area_name='南沙区',area_ctime=datetime.now()),
        Hous_area(area_id=10,area_name='增城区',area_ctime=datetime.now()),
        Hous_area(area_id=11,area_name='从化区',area_ctime=datetime.now()),
    ])


    dbSession.add_all([
        Facility(id=1, name='无线网络', cretetime=datetime.now()),
        Facility(id=2, name='热水淋浴', cretetime=datetime.now()),
        Facility(id=3, name='空调', cretetime=datetime.now()),
        Facility(id=4, name='暖气', cretetime=datetime.now()),
        Facility(id=5, name='允许吸烟', cretetime=datetime.now()),
        Facility(id=6, name='饮水设备', cretetime=datetime.now()),
        Facility(id=7, name='牙具', cretetime=datetime.now()),
        Facility(id=8, name='香皂', cretetime=datetime.now()),
        Facility(id=9, name='拖鞋', cretetime=datetime.now()),
        Facility(id=10, name='手纸', cretetime=datetime.now()),
        Facility(id=11, name='毛巾', cretetime=datetime.now()),
        Facility(id=12, name='沐浴露、洗发露', cretetime=datetime.now()),
        Facility(id=13, name='冰箱', cretetime=datetime.now()),
        Facility(id=14, name='洗衣机', cretetime=datetime.now()),
        Facility(id=15, name='电梯', cretetime=datetime.now()),
        Facility(id=16, name='允许做饭', cretetime=datetime.now()),
        Facility(id=17, name='允许带宠物', cretetime=datetime.now()),
        Facility(id=18, name='允许聚会', cretetime=datetime.now()),
        Facility(id=19, name='门禁系统', cretetime=datetime.now()),
        Facility(id=20, name='停车位', cretetime=datetime.now()),
        Facility(id=21, name='有线网络', cretetime=datetime.now()),
        Facility(id=22, name='电视', cretetime=datetime.now()),
        Facility(id=23, name='浴缸', cretetime=datetime.now())
    ])
    dbSession.commit()


if options.s: create_h()
print'添加数据成功'