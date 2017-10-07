#coding=utf-8
import re
import logging

import tornado.web

from BaseHandler import BaseHandler
from utils.response_code import RET
from models.sql import Tenant





class MYHandler(BaseHandler):
    '我的房源/myhouse'
    @tornado.web.authenticated
    def get(self):
        T = Tenant.by_mobile(self.current_user.phone_number)
        self.render("my.html",
                    user_avatar=T.user_avatar,
                    name=T.name,
                    phone_number=self.current_user.phone_number,
                    )


class AuthHandler(BaseHandler):
    '实名认证/my/auth'
    @tornado.web.authenticated
    def get(self):
        self.render("auth.html")

    def post(self):
        real_name = self.get_argument('real_name','')
        id_card = self.get_argument('id_card','')

        if not all((real_name,id_card)):
            return self.write(dict(errno=RET.PARAMERR, errmsg='确少数据'))

        user = Tenant.by_mobile(self.current_user.phone_number)
        if user.real_name and id_card:
            return self.write(dict(errno=RET.DATAEXIST, errmsg='数据已存在不能添加'))

        if not re.match(r'^([1-9]\d{5}[12]\d{3}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])\d{3}[0-9xX])$',id_card):
            return self.write(dict(errno=RET.ROLEERR, errmsg='用户身份错误'))

        try:
            user = Tenant.by_mobile(self.current_user.phone_number)
            user.real_name = real_name
            user.id_card = id_card
            self.db.add(user)
            self.db.commit()
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg='参数错误'))
        return self.write(dict(errcode=RET.OK, errmsg='OK'))




class LogoutHandler(BaseHandler):
    '退出登录/my'
    def get(self):
        self.session.delete('user')
        self.redirect('/login')