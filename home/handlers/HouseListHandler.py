#coding=utf-8
import tornado.web
from sqlalchemy import text,and_,or_,not_,func,extract,exists
from models.sql import Hous_info,Tenant,Order_info,Hous_area

from BaseHandler import BaseHandler


class SearchHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        global Hous_info
        global housinfo
        H_area = self.db.query(Hous_area).all()
        area_id = self.get_argument('area_id','')               #区域
        start_date = self.get_argument('start-date','')         #入住时间
        end_date = self.get_argument('end-date','')             #离开时间
        sort_key = self.get_argument('sort_key','new')          #别的条件


        if (start_date and end_date):
            D_data = (start_date - end_date)
            housinfo = self.db.query(Hous_info).filter(and_(Hous_info.hi_min_days < D_data), Hous_info.on_line == 1).all()
        if area_id:
            housinfo = self.db.query(Hous_info).filter(and_(Hous_info.on_line == 1,Hous_info.hous_areaid == area_id)).all()
        if sort_key:
            if "new" == sort_key:  # 按最新上传时间排序
                housinfo = self.db.query(Hous_info).filter(Hous_info.on_line == 1).order_by(-Hous_info.ctime).all()
            elif "booking" == sort_key:  # 最受欢迎
                housinfo = self.db.query(Hous_info).filter(Hous_info.on_line == 1).order_by(Hous_info.order_count).all()
            elif "price-inc" == sort_key:  # 价格由低到高
                housinfo = self.db.query(Hous_info).filter(Hous_info.on_line == 1,).order_by(-Hous_info.price).all()
            elif "price-des" == sort_key:  # 价格由高到低
                housinfo = self.db.query(Hous_info).filter(Hous_info.on_line == 1,).order_by(Hous_info.price).all()

        if (start_date and end_date) and area_id and sort_key:              # 时间
            D_data = (start_date - end_date)
            if sort_key:
                if "new" == sort_key :          # 按最新上传时间排序
                    housinfo = self.db.query(Hous_info).filter(and_(Hous_info.hi_min_days < D_data),Hous_info.on_line == 1,Hous_info.hous_areaid==area_id).order_by(-Hous_info.ctime).all()
                elif "booking"== sort_key :     # 最受欢迎
                    housinfo = self.db.query(Hous_info).filter(and_(Hous_info.hi_min_days < D_data),Hous_info.on_line == 1,Hous_info.hous_areaid == area_id).order_by(Hous_info.order_count).all()
                elif "price-inc" == sort_key:   # 价格由低到高
                    housinfo = self.db.query(Hous_info).filter(and_(Hous_info.hi_min_days < D_data),Hous_info.on_line == 1,Hous_info.hous_areaid == area_id).order_by(-Hous_info.price).all()
                elif "price-des" == sort_key:   # 价格由高到低
                    housinfo = self.db.query(Hous_info).filter(and_(Hous_info.hi_min_days < D_data),Hous_info.on_line == 1,Hous_info.hous_areaid == area_id).order_by(Hous_info.price).all()

        elif (start_date and end_date) and area_id:
            D_data = (start_date - end_date)
            housinfo = self.db.query(Hous_info).filter(and_(Hous_info.hi_min_days < D_data), Hous_info.on_line == 1,Hous_info.hous_areaid == area_id).all()

        elif (start_date and end_date) and sort_key:
            D_data = (start_date - end_date)
            if sort_key:
                if "new" == sort_key :          # 按最新上传时间排序
                    housinfo = self.db.query(Hous_info).filter(and_(Hous_info.hi_min_days < D_data),Hous_info.on_line == 1).order_by(-Hous_info.ctime).all()
                elif "booking"== sort_key :     # 最受欢迎
                    housinfo = self.db.query(Hous_info).filter(and_(Hous_info.hi_min_days < D_data),Hous_info.on_line == 1).order_by(Hous_info.order_count).all()
                elif "price-inc" == sort_key:   # 价格由低到高
                    housinfo = self.db.query(Hous_info).filter(and_(Hous_info.hi_min_days < D_data),Hous_info.on_line == 1).order_by(-Hous_info.price).all()
                elif "price-des" == sort_key:   # 价格由高到低
                    housinfo = self.db.query(Hous_info).filter(and_(Hous_info.hi_min_days < D_data),Hous_info.on_line == 1).order_by(Hous_info.price).all()

        elif area_id and sort_key:
            if sort_key:
                if "new" == sort_key :          # 按最新上传时间排序
                    housinfo = self.db.query(Hous_info).filter(and_(Hous_info.on_line == 1),Hous_info.hous_areaid==area_id).order_by(-Hous_info.ctime).all()
                elif "booking"== sort_key :     # 最受欢迎
                    housinfo = self.db.query(Hous_info).filter(and_(Hous_info.on_line == 1),Hous_info.hous_areaid == area_id).order_by(Hous_info.order_count).all()
                elif "price-inc" == sort_key:   # 价格由低到高
                    housinfo = self.db.query(Hous_info).filter(and_(Hous_info.on_line == 1),Hous_info.hous_areaid == area_id).order_by(-Hous_info.price).all()
                elif "price-des" == sort_key:   # 价格由高到低
                    housinfo = self.db.query(Hous_info).filter(and_(Hous_info.on_line == 1),Hous_info.hous_areaid == area_id).order_by(Hous_info.price).all()

        else:  # In什么都没有
            housinfo = self.db.query(Hous_info).filter(Hous_info.on_line == 1).order_by(-Hous_info.ctime).all()
        self.render("search.html", H_area=H_area, hous_info=housinfo)


