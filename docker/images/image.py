# -*- coding: utf-8 -*-
import json
import tornado
from tornado.httpclient import AsyncHTTPClient


class ImageHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        http = tornado.httpclient.AsyncHTTPClient()
        http.fetch("http://10.0.31.82:4243/containers/json",
                   callback=self.on_response)
    
    def on_response(self, response):
        if response.error: raise tornado.web.HTTPError(500)
        images = json.loads(response.body)
        self.render("image/list.html", images=images)
        
        
    
