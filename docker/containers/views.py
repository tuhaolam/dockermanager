#coding: utf-8
import json
import functools
import random
import tornado
from tornado.httpclient import AsyncHTTPClient
from tornado.util import ObjectDict
from tornado.httputil import HTTPHeaders
from hosts.views import BaseHandler

class ContainerHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self,hid,cid):
        http = tornado.httpclient.AsyncHTTPClient()
        host = self.db.query("SELECT * FROM host WHERE id= %s",int(hid))[0]
        cb = functools.partial(self.on_response_dict,hid=hid)
        http.fetch("http://%s:%d/containers/%s/json" % (host.hostname,host.port,cid),
                   callback=cb)
    def on_response_dict(self,response,hid):
        if response.error:raise tornado.web.HTTPError(500)
        obj = json.loads(response.body)
        self.render('container/detail.html',hid=hid,container=ObjectDict(obj))

    def on_op(self,response,hid,cid):
        if response.error:raise tornado.web.HTTPError(500)
        response.headers.clear()
        self.redirect('/containers/%s/%s' %(hid,cid))

    def on_redirect_container_list(self,response,hid):
        if response.error: raise tornado.web.HTTPError(500)
        self.redirect('/containers/?host=%s'%(hid,))
    @tornado.web.asynchronous
    def post(self,hid,cid,op):
        http = tornado.httpclient.AsyncHTTPClient()
        host = self.db.query("SELECT * FROM host WHERE id= %s",int(hid))[0]
        cb = functools.partial(self.on_op,hid=hid,cid=cid)
        h = HTTPHeaders({"content-type": 'application/json'})
        if op=='stop':
            http.fetch("http://%s:%d/containers/%s/stop?t=5" % (host.hostname,host.port,cid),
                   callback=cb,method='POST',body="")
        elif op=='start':
            http.fetch("http://%s:%d/containers/%s/start?t=5" % (host.hostname,host.port,cid),
                   callback=cb,headers=h,method='POST',body='{"PublishAllPorts":true}')
        elif op=='restart':
            http.fetch("http://%s:%d/containers/%s/restart?t=5" % (host.hostname,host.port,cid),
                   callback=cb,method='POST',body="")
        elif op =='delete':
            cb = functools.partial(self.on_redirect_container_list,hid=hid)
            http.fetch("http://%s:%d/containers/%s?force=1" % (host.hostname,host.port,cid),
                   callback=cb,method='DELETE')



class ContainerDeployHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self,hid):
        http = tornado.httpclient.AsyncHTTPClient()
        host = self.db.query("SELECT * FROM host WHERE id= %s",int(hid))[0]
        cb = functools.partial(self.on_response_dict,hid=hid)
        http.fetch("http://%s:%d/images/json" % (host.hostname,host.port),
                   callback=cb)
    def on_response_dict(self,response,hid):
        if response.error:raise tornado.web.HTTPError(500)
        obj = json.loads(response.body)
        self.render('container/add.html',hid=hid,images=[ObjectDict(image) for image in obj])


class ContainerListHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        http = tornado.httpclient.AsyncHTTPClient()
        hostid = self.get_argument('host',None)
        host = self.db.query("SELECT * FROM host WHERE id= %s",int(hostid))[0]
        http.fetch("http://%s:%d/containers/json?all=1" % (host.hostname,host.port),
                   callback=functools.partial(self.on_response,hid=host.id))

    def on_response(self, response,hid):
        if response.error: raise tornado.web.HTTPError(500)
        objs = json.loads(response.body)
        self.render("container/list.html",hid=hid, containers=[ObjectDict(obj) for obj in objs])

    def on_redirect_container_list(self,response,hid):
        if response.error: raise tornado.web.HTTPError(500)
        self.redirect('/containers/?host=%s'%(hid,))


    @tornado.web.asynchronous
    def post(self):
        http = tornado.httpclient.AsyncHTTPClient()
        hostid = self.get_argument('host',None)
        name = self.get_argument('name',None)
        image = self.get_argument('image',None)
        host = self.db.query("SELECT * FROM host WHERE id= %s",int(hostid))[0]
        h = HTTPHeaders({"content-type": "application/json"})
        url= "http://%s:%d/containers/create"
        if name:
            url=url+"?name="+name
        http.fetch(url % (host.hostname,host.port),
                   callback=functools.partial(self.on_redirect_container_list,hid=host.id),headers=h,
                   method='POST',body='{"Image":"%s","Hostname":"xx1","AttachStdin":true}' %(image,))
