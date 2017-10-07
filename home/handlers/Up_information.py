#coding=utf-8

import logging
import tornado.web

from BaseHandler import BaseHandler
from utils.response_code import RET
from utils.qiniu_storage import storage
from  models.sql import Tenant
import constants



class Up_informationHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("profile.html")


class AvatrHandler(BaseHandler):
    """上传头像"""
    @tornado.web.authenticated
    def post(self):
        try:
            image_data = self.request.files.get('avatar','')
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.PARAMERR, errmsg="未传图片"))
        try:
            file_name = storage(image_data[0]["body"])
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.THIRDERR, errmsg="上传失败"))
        try:
            user = Tenant.by_mobile(self.current_user.phone_number)
            user.user_avatar = file_name
            self.db.add(user)
            self.db.commit()
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg="保存错误"))
        self.write(dict(errcode=RET.OK, errmsg="保存成功", data="%s%s" % (constants.QINIU_URL_PREFIX, file_name)))



class NameHandler(BaseHandler):
    """用户名"""
    @tornado.web.authenticated
    def post(self):
        name = self.get_argument('name','')
        if name in (None,''):
            return self.write(dict(errcode=RET.PARAMERR,errmsq='参数错误'))
        try:
            user = Tenant.by_mobile(self.current_user.phone_number)
            user.name = name
            self.db.add(user)
            self.db.commit()
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg='参数错误'))
        return self.write(dict(errcode=RET.OK, errmsg='OK'))



