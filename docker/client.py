# -*- coding: utf-8 -*-
"""
Created on Sun Sep 28 09:34:44 2014

@author: aaron
"""
from tornado.httpclient import AsyncHTTPClient
from tornado import gen

@gen.coroutine
def fetch_coroutine(url):
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url)
        
    print response.body
    yield response.body
    return
    
    
if __name__ =='__main__':
    print fetch_coroutine('http://10.0.31.82:4243/containers/json')