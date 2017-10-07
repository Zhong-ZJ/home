#coding=utf-8
import random
import re
from datetime import datetime

import tornado.web
import logging

from BaseHandler import BaseHandler
from pillow_text import pillow_test

from models.sql import Tenant,Hous_area,Hous_info,Order_info
from utils.response_code import RET
import constants
from libs.yun_tong_xin.yun_tong_xin import sendTemplateSMS
from sqlalchemy import text,and_,or_,not_,func,extract,exists

class RegisterHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.redirect('/index')
        else:
            self.render('register.html')

    def post(self):
        user = self.get_argument('mobile', '')          # 手机号
        phonecode = self.get_argument('phonecode', '')  # 手机验证码
        password2 = self.get_argument('password', '')   # 密码
        print user,phonecode,password2
        # 检查参数
        if not all([user, phonecode, password2]):
            return self.write(dict(errcode=RET.PARAMERR, errmsg="参数不完整"))
        # 判断手机号格式
        if not re.match(r"^1\d{10}$",user):
            return self.write(dict(errcode=RET.DATAERR, errmsg="手机号格式错误"))
        # 检查验证码获取是否成功
        try:
            real_sms_code = self.redis.get(user)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg="查询验证码出错"))
        # 检查验证码是否过期
        if not real_sms_code:
            return self.write(dict(errcode=RET.NODATA, errmsg="验证码过期"))
        # 检查验证码是否错误
        if real_sms_code != phonecode:
            return self.write(dict(errcode=RET.DATAERR, errmsg="验证码错误"))

        # 检查手机是否被注册
        if Tenant.by_mobile(user):
            return self.write(dict(errcode=RET.DATAEXIST, errmsg="已注册"))

        T = Tenant()
        T.phone_number = self.get_argument('mobile', '')
        T.password = self.get_argument('password', '')
        T.createtime = datetime.now()
        T.updatetime = datetime.now()
        self.db.add(T)
        self.db.commit()
        self.write(dict(errcode=RET.OK, errmsg="注册成功"))



class TestHandler(BaseHandler):
    def get(self):
        pre_code = self.get_argument('pre_code', '')            #旧
        code = self.get_argument('code', '')                    #新
        if pre_code:
            self.redis.delete(pre_code)
            img,text = pillow_test()
            self.redis.setex(code,text,1800)                      #code键(图片验证码),text值(图片验证码字符),60过期时间
            self.set_header('Content-Type','image/jpg')
            self.write(img)


class SMS_authHandler(BaseHandler):
    def post(self):
        #'''获取参数'''
        mobile = self.get_argument('mobile','')                               #手机号
        image_code_id = self.get_argument('image_code_id','')                 #图片的验证码
        image_code_text = self.get_argument('image_code_text','')             #输入的验证码

        print mobile,image_code_id,image_code_text
        if not all((mobile,image_code_id,image_code_text)):
            return self.write(dict(errno=RET.PARAMERR, errmsg='参数不完整!'))
        if not re.match(r'1\d{10}',mobile):
            return self.write(dict(errno=RET.PARAMERR, errmsg='手机号错误!'))

        #'''判断图片验证码'''
        try:
            real_image_code_text = self.redis.get(image_code_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR,errmsg='查询出错!'))
        if not real_image_code_text:
            return self.write(dict(errno=RET.NODATA,errmsg='验证码已过期!'))
        if real_image_code_text.lower() != image_code_text.lower():
            return self.write(dict(errno=RET.DATAERR,errmsg='验证码错误!'))

        #'''若成功生成随机验证码'''
        sms_code = '%04d' % random.randint(0,9999)
        try:
            self.redis.setex(mobile,sms_code,constants.SMS_CODE_EXPIRES_SECONDS)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DATAERR, errmsg="生成短信验证码错误!"))

        #'''发生短信'''
        try:
            sendTemplateSMS(mobile, [sms_code,30], 1)
            self.write(dict(errno=RET.OK, errmsg='OK'))

        #'''需要判断返回值，待实现'''
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.THRDERR,errmsg='发送失败!'))




class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        mobile = Tenant.by_mobile(self.get_argument('mobile', ''))
        password = self.get_argument('password','')
        print mobile,password
        if mobile and mobile.auth_password(password):
            try:
                self.session.set('user',mobile.phone_number)
            except Exception as e:
                logging.error(e)
            self.redirect('/index')
        else:
            return self.write(dict(errcode=RET.DATAERR, errmsg="手机号或密码错误！"))






class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        H_area = self.db.query(Hous_area).all()
        H_info = self.db.query(Hous_info).filter(Hous_info.on_line == 1).order_by(-Hous_info.ctime).limit(5).offset(0).all()
        self.render("index.html",H_area = H_area,H_info=H_info)














