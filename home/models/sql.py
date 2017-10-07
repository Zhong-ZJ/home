#coding=utf-8
from uuid import uuid4
from datetime import datetime
from pbkdf2 import PBKDF2
from sqlalchemy.orm import relationship
from sqlalchemy import (create_engine, Column, Integer, String,Text, Boolean, Date, DateTime, ForeignKey)
from sqlalchemy.types import Integer
from libs.db.dbsession import Base,dbSession

#房客信息表
class Tenant(Base):
    __tablename__ = 'tenant'
    id = Column(Integer,nullable=False,autoincrement=True,primary_key=True)         #用户ID
    name = Column(String(32),unique=True)                                           #昵称
    phone_number = Column(String(11),nullable=False,unique=True)                    #手机号
    _password = Column(String(64),nullable=False)                                   #密码
    real_name = Column(String(32))                                                  #真实姓名
    id_card = Column(String(20),unique=True)                                        #身份证号
    user_avatar = Column(String(128))                                               #用户头像
    admin = Column(String(1),nullable=False,default=int(0))                         #管理员 1为是 0为不是
    createtime = Column(DateTime,nullable=False,default=datetime.now())             #创建时间
    updatetime = Column(DateTime,nullable=False)                                    #更新时间
    hous_info = relationship('Hous_info',backref='tenants')
    order_info = relationship('Order_info')

    def _hash_password(self,password):
        return PBKDF2.crypt(password,iterations=0x2537)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,password):
        self._password = self._hash_password(password)

    def auth_password(self, other_password):
        if self._password:
            return self.password == PBKDF2.crypt(other_password, self.password)
        else:
            return False

    @classmethod
    def by_mobile(cls, mobile):
        return dbSession.query(cls).filter_by(phone_number=mobile).first()

    @classmethod
    def by_mobile_one(cls, mobile):
        return dbSession.query(cls).filter_by(phone_number=mobile)

    @classmethod
    def by_name(cls, name):
        return dbSession.query(cls).filter_by(username=name).first()    #filter_by = where

    @classmethod
    def by_password(cls,password):
        return dbSession.query(cls).filter_by(_password=password).first()


#房源区域表
class Hous_area(Base):
    __tablename__ = 'hous_area'
    area_id = Column(Integer,nullable=False,autoincrement=True,primary_key=True)        #区域ID
    area_name = Column(String(32),nullable=False)                                       #区域名称                                                            #管理员 1为是 0为不是
    area_ctime = Column(DateTime,nullable=False,default=datetime.now())                 #创建时间
    hous_info = relationship('Hous_info')



#房屋信息与设施中间表
class Info_to_Facility(Base):
    __tablename__ = 'info_to_facility'
    house_id = Column(Integer,ForeignKey('hous_info.hous_id'),primary_key=True)         #房屋ID
    facility_id = Column(Integer,ForeignKey('facility.id'),primary_key=True)            #房屋设施
    ctime = Column(DateTime,nullable=False,default=datetime.now())                      #创建时间


# 房屋信息表
class Hous_info(Base):
    __tablename__ = 'hous_info'
    hous_id = Column(Integer,autoincrement=True,primary_key=True,nullable=False)    #房屋ID
    name = Column(String(64),nullable=False)                                        #房屋名称
    price = Column(Integer,nullable=False,default=int(0))                           #房价
    site = Column(String(512),nullable=False,default='')                            #地址
    room_count = Column(Integer,nullable=False,default=int(1))                      #房间数量
    acreage = Column(Integer,nullable=False,default=int(0))                         #房屋面积
    type = Column(String(32),nullable=False,default='')                             #房屋户型
    capacity = Column(Integer,nullable=False,default=int(1))                        #容纳人数
    bed = Column(String(64),nullable=False,default='')                              #床配置
    deposit = Column(Integer,nullable=False,default=int(0))                         #押金,单位分
    min_days = Column(Integer,nullable=False,default=int(1))                        #最短入住时间
    max_days = Column(Integer,nullable=False,default=int(0))                        #最长入住时间，0-不限制
    order_count = Column(Integer,nullable=False,default=int(0))                     #下单数量
    verify_status = Column(Integer,nullable=False,default=int(0))                   #审核状态，0-待审核，1-审核未通过，2-审核通过
    on_line = Column(Integer,nullable=False,default=int(1))                         #0-下线，1-上线
    image_url = Column(String(256),nullable=False)                                  #房屋主图片url
    ctime = Column(DateTime,nullable=False)                                         #创建时间
    updatetime = Column(DateTime,nullable=False,default=datetime.now())             #更新时间

    tenant = relationship('Tenant',backref='hous_infos')                            #房屋id与用户id       一对多
    tenant_id = Column(Integer, ForeignKey('tenant.id'))

    hous_area = relationship('Hous_area')                                           #房屋区域id与区域id    一对多
    hous_areaid = Column(Integer,ForeignKey('hous_area.area_id'))

    info_facility = relationship('Facility', secondary=Info_to_Facility.__table__)  #多对多

    order_info = relationship('Order_info')

    @classmethod
    def by_hous_id(cls,id):
        return dbSession.query(cls).filter_by(hous_id=id).first()




#设施型录表
class Facility(Base):
    __tablename__ = 'facility'
    id = Column(Integer,nullable=False,autoincrement=True,primary_key=True)             #自增ID
    name = Column(String(32),nullable=False)                                            #设施名称
    cretetime = Column(DateTime,nullable=False,default=datetime.now())                  #创建时间
    facility_info = relationship('Hous_info', secondary=Info_to_Facility.__table__)

    @classmethod
    def by_id(cls,id):
        return dbSession.query(cls).filter_by(id=id).one()



#订单表
class Order_info(Base):
    __tablename__ = 'order_info'
    order_id = Column(Integer,nullable=False,autoincrement=True,primary_key=True)   #订单ID
    order_begin_date = Column(String(32),nullable=False)                            #入住时间
    order_end_date = Column(String(32),nullable=False)                              #离开时间
    order_cheak_days = Column(Integer,nullable=False)                               #入住天数
    order_house_price = Column(Integer,nullable=False)                              #房屋单价，单位分
    order_amount = Column(Integer,nullable=False)                                   #订单金额，单位分
    order_status = Column(Integer,nullable=False,default=int(0))                    #订单状态，0-待接单，1-待支付，2-已支付，3-待评价，4-已完成，5-已取消，6-拒接单'
    order_message = Column(Text)                                                    #订单评论
    order_ctime = Column(DateTime,nullable=False,default=datetime.now())            #创建时间
    order_utime = Column(DateTime,nullable=False)                                   #更新时间

    tenant = relationship('Tenant')
    tenant_id = Column(Integer, ForeignKey('tenant.id'))

    hous_info = relationship('Hous_info',backref='hous_info')
    hous_info_id = Column(Integer, ForeignKey('hous_info.hous_id'))









