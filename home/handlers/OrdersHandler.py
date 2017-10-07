#coding=utf-8

import logging
from datetime import datetime
import tornado.web
# from sqlalchemy import text,and_,or_,not_,func,extract,exists,in_

from BaseHandler import BaseHandler
from models.sql import Hous_info,Order_info,Tenant
from utils.response_code import RET

class BookingHandler(BaseHandler):
    '''预订'''
    @tornado.web.authenticated
    def get(self):
        id = self.get_argument('id','')
        hous_info = self.db.query(Hous_info).filter(Hous_info.hous_id==id).first()
        self.render('booking.html',Hous_info=hous_info)

    def post(self):
        user = self.current_user.phone_number
        house_id = self.get_argument('house_id','')
        start_date = self.get_argument('start_date','')
        end_date = self.get_argument('end_date','')
        amount = self.get_argument('amount','')
        price = self.get_argument('price','')

        d1 = datetime.strptime(start_date,'%Y-%m-%d')
        d2 = datetime.strptime(end_date,'%Y-%m-%d')
        days = (d2-d1).days +1

        if not all((house_id,start_date,end_date,amount)):
            return self.write(dict(errcode=RET.PARAMERR,errmsg="参数错误"))

        user = Tenant.by_mobile(user)
        if int(house_id) in [i.hous_id for i in user.hous_info]:
            return self.write(dict(errcode=RET.PARAMERR, errmsg="自己房子不能下单"))

        try:
            order = Order_info()
            order.order_begin_date = start_date
            order.order_end_date = end_date
            order.order_cheak_days = days
            order.order_house_price = price
            order.order_amount = amount
            order.tenant_id = user.id
            order.hous_info_id = house_id
            order.order_utime = datetime.now()
            self.db.add(order)
            self.db.commit()
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg="save data error"))
        self.write(dict(errcode=RET.OK, errmsg="OK"))


class OrdersHandler(BaseHandler):
    '''我的订单'''
    @tornado.web.authenticated
    def get(self):
        user = Tenant.by_mobile(self.current_user.phone_number)
        oders = self.db.query(Order_info).filter(Order_info.tenant_id == user.id).all()
        self.render("orders.html",oders=oders)



class LordersHandler(BaseHandler):
    '''客户订单'''
    @tornado.web.authenticated
    def get(self):
        user = Tenant.by_mobile(self.current_user.phone_number)
        lorders = self.db.query(Order_info).filter(Order_info.hous_info_id.in_([i.hous_id for i in user.hous_info]) ).all()
        self.render("lorders.html",lorders=lorders )



class AcceptOrderHandler(BaseHandler):
    """接单"""
    @tornado.web.authenticated
    def post(self):
        # 处理的订单编号
        order_id = self.get_argument("order_id",'')

        if not order_id:
            return self.write(dict(errcode=RET.PARAMERR, errmsg="参数错误"))

        order_info = self.db.query(Order_info).filter(Order_info.order_id == order_id).first()
        try:
            # 确保房东只能修改属于自己房子的订单
            order_info.hous_info.on_line = 0
            order_info.hous_info.order_count += 1
            order_info.order_status = 4
            order_info.order_utime = datetime.now()
            self.db.add(order_info)
            self.db.commit()
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg="数据库错误"))
        self.write(dict(errcode=RET.OK, errmsg="OK"))




class RejectOrderHandler(BaseHandler):
    """拒单"""
    @tornado.web.authenticated
    def post(self):
        order_id = self.get_argument("order_id", '')
        reject_reason = self.get_argument("reject_reason",'')

        if not all((order_id, reject_reason)):
            return self.write(dict(errcode=RET.PARAMERR, errmsg="参数错误"))

        try:
            order_info = self.db.query(Order_info).filter(Order_info.order_id == order_id).first()
            order_info.order_status = 6
            order_info.order_message = reject_reason
            order_info.order_utime = datetime.now()
            self.db.add(order_info)
            self.db.commit()
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg="数据库错误"))
        self.write(dict(errcode=RET.OK, errmsg="OK"))





class OrderCommentHandler(BaseHandler):
    """评论"""
    @tornado.web.authenticated
    def post(self):
        user = Tenant.by_mobile(self.current_user.phone_number)
        order_id = self.get_argument("order_id", '')
        comment = self.get_argument("comment", '')

        if not all((order_id, comment)):
            return self.write(dict(errcode=RET.PARAMERR, errmsg="参数错误"))

        try:
            # 需要确保只能评论自己下的订单
            order_info = self.db.query(Order_info).filter(Order_info.order_id == order_id).first()
            order_info.order_message = comment
            self.db.add(order_info)
            self.db.commit()
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg="数据库错误"))
        self.write(dict(errcode=RET.OK, errmsg="OK"))