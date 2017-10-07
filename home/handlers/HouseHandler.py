#coding=utf-8
import logging
import json
from datetime import datetime

import redis
import tornado.web

from BaseHandler import BaseHandler
from models.sql import Tenant,Hous_area,Info_to_Facility,Hous_info,Facility
import constants
from utils.response_code import RET
from utils.qiniu_storage import storage



class MyHousesHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = self.current_user.phone_number
        T = Tenant.by_mobile(user)
        self.render('myhouse.html',T=T)

class DetailHandler(BaseHandler):
    def get(self):
        id = self.get_argument('id')
        house = Hous_info.by_hous_id(id)
        user = self.current_user.phone_number
        self.render("detail.html",house=house,user=user)


class NewhouseHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        H_area = self.db.query(Hous_area).all()
        facility = self.db.query(Facility).all()
        self.render("newhouse.html",H_area=H_area,facility=facility)

    def post(self):
        #'''In[基本信息]'''
        house_title = self.get_argument('house_title','')                   #房屋标题
        one_night_price = int(self.get_argument('one_night_price',''))      #每晚价格
        area_id = int(self.get_argument('area_id',''))                      #所在城区
        address = self.get_argument('address','')                           #详细地址

        #'''In[详细信息]'''
        room_count = int(self.get_argument('room_count',''))                #出租房间数目
        aacreage = int(self.get_argument('acreage',''))                     #房屋面积
        unit = self.get_argument('unit','')                                 #户型描述
        capacity = int(self.get_argument('capacity',''))                    #宜住人数
        beds = self.get_argument('beds','')                                 #卧床配置
        deposit = int(self.get_argument('deposit',''))                      #押金数额
        min_days = int(self.get_argument('min_days',''))                    #最少入住天数
        max_days = int(self.get_argument('max_days',''))                    #最多入住天数
        facility = self.get_body_arguments('facility[]', '')                #配套设施
        himage = self.request.files.get('house_image', '')                  #获取图片

        if not all((house_title,one_night_price,area_id,address,room_count,aacreage,unit,capacity,beds,deposit,min_days,himage)):
            return self.write(dict(errcode=RET.DATAERR,errmsg="缺少参数"))

        if max_days == 0 and min_days < 0:
            return self.write(dict(errcode=RET.DATAERR, errmsg="最多入住天数等于0时，入住最少天数不应比0小"))

        if max_days > 0 and min_days > max_days:
            return self.write(dict(errcode=RET.DATAERR, errmsg="最多入住天数应大于最少入住天数"))

        # '''In[保存图片]'''
        try:
            T = Tenant.by_mobile(self.current_user.phone_number)
            hous_info = Hous_info()
            hous_info.tenant_id= T.id                       #保存房东ID(外键)
            hous_info.name = house_title                    #保存房屋名称
            hous_info.price = one_night_price               #保存每晚价格
            hous_info.hous_areaid = area_id                 #保存区域ID(外键)
            hous_info.site = address                        #保存地址
            hous_info.room_count = room_count               #保存房间数量
            hous_info.acreage = aacreage                    #保存房屋面积
            hous_info.type  = unit                          #保存房屋
            hous_info.capacity  = capacity                  #保存户型描述
            hous_info.bed  = beds                           #保存床配置
            hous_info.deposit  = deposit                    #保存押金
            hous_info.min_days  = min_days                  #保存最小天数
            hous_info.max_days  = max_days                  #保存最大天数
            hous_info.ctime = datetime.now()                #保存创建时间

            # 房屋与配套设施中间表
            try:
                for i in facility:
                    facilitys = Facility.by_id(i)
                    hous_info.info_facility.append(facilitys)
            except Exception as e:
                logging.error(e)
                return self.write(dict(errcode=RET.PARAMERR, errmsg='配套设施参数错误'))

            try:
                file_name = storage(himage[0]['body'])
                hous_info.image_url = (constants.QINIU_URL_PREFIX + file_name)          #图片路径
            except Exception as e:
                logging.error(e)
                return self.write(dict(errcode=RET.PARAMERR, errmsg='图片保存错误'))

            self.db.add(hous_info)
            self.db.commit()
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.PARAMERR, errmsg='hous_info参数错误'))
        self.write(dict(errno=RET.OK, errmsg='OK'))























