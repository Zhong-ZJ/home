#coding=utf-8
import json
import redis
from tornado.web import RequestHandler
from libs.pycket.session import SessionMixin
from libs.db.dbsession import dbSession
from models.sql import Tenant

class BaseHandler(RequestHandler,SessionMixin):
    def initialize(self):
        self.db = dbSession
        self.redis = redis.Redis()

    def get_current_user(self):
        if self.session.get('user'):
            return Tenant.by_mobile(self.session.get('user'))
        else:
            return None

    def write_error(self, status_code, **kwargs):
        pass

    def on_finish(self):
        self.db.close()




