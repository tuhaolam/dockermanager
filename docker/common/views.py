#coding: utf-8
__author__ = 'aaron'
import tornado
class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

