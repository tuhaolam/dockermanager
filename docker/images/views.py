#coding: utf-8
import json
import functools
import base64
import tornado
from tornado.httpclient import AsyncHTTPClient
from tornado.util import ObjectDict
from tornado.httputil import HTTPHeaders
from hosts.views import BaseHandler
class ImageListHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        http = tornado.httpclient.AsyncHTTPClient()
        hid = self.get_argument('host',None)
        host = self.db.query("SELECT * FROM host WHERE id= %s",int(hid))[0]
        cb=functools.partial(self.on_response,hid=host.id)
        http.fetch("http://%s:%d/images/json" % (host.hostname,host.port),
                   callback=cb)

    def on_response(self, response,hid):
        if response.error: raise tornado.web.HTTPError(500)
        images = json.loads(response.body)
        self.render("image/list.html",hid=hid, images=[ObjectDict(image) for image in images])
    def on_redirect(self,response,hid):
        if response.error: raise tornado.web.HTTPError(500)
        self.redirect('/images/?host='+hid)
    @tornado.web.asynchronous
    def post(self):
        http = tornado.httpclient.AsyncHTTPClient()
        hid = self.get_argument('host',None)
        host = self.db.query("SELECT * FROM host WHERE id= %s",int(hid))[0]
        authconifg='{"username":"aaron315","password":"aaron@bj", "auth":"","email":"guowei13217962163.com"}'
        h = HTTPHeaders({"X-Registry-Auth": base64.b64encode(authconifg)})
        http.fetch('http://%s:%d/images/create?fromImage=10.0.31.82:5000&repo=tutum/redis'%(host.hostname,host.port),
                   headers=h,method='POST',body="",
                   callback=functools.partial(self.on_redirect,hid=hid))

class ImageHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self,hid,iid):
        http = tornado.httpclient.AsyncHTTPClient()
        host = self.db.query("SELECT * FROM host WHERE id= %s",int(hid))[0]
        http.fetch("http://%s:%d/images/%s/json" % (host.hostname,host.port,iid),
                   callback=functools.partial(self.on_response_dict,hid=hid))
    def on_response_dict(self,response,hid):
        if response.error:raise tornado.web.HTTPError(500)
        obj = json.loads(response.body)
        self.render('image/detail.html',image=ObjectDict(obj),hid=hid)

    @tornado.web.asynchronous
    def post(self,hid,iid,op):
        http = tornado.httpclient.AsyncHTTPClient()
        host = self.db.query("SELECT * FROM host WHERE id= %s",int(hid))[0]
        cb = functools.partial(self.on_op,hid=hid)
        if op=='delete':
            http.fetch("http://%s:%d/images/%s" % (host.hostname,host.port,iid),
                   callback=cb,method='DELETE')

    def on_op(self,response,hid):
        if response.error:raise tornado.web.HTTPError(500)
        self.redirect('/images/?host=%s'%(hid,))
