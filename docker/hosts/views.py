#coding: utf-8
__author__ = 'aaron'
import json
import tornado
from tornado.httpclient import AsyncHTTPClient

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db
class HostHandler(BaseHandler):
    def get(self):
        id = self.get_argument('id',None)
        host =None
        if id:
            host = self.db.query("SELECT * FROM host WHERE id= %s",int(id))[0]
        self.render("host/host.html", host=host)

    def post(self):
        id = self.get_argument("id", None)
        name = self.get_argument("name")
        hostname = self.get_argument("hostname")
        public_hostname = self.get_argument('public_hostname')
        agent_key = self.get_argument('agent_key')
        port = self.get_argument('port')
        if id:
            host = self.db.get("SELECT * FROM host WHERE id = %s", int(id))
            if not host: raise tornado.web.HTTPError(404)
            self.db.execute(
                "UPDATE host SET name = %s, hostname = %s, public_hostname = %s "
                ",agent_key = %s, port = %s "
                "WHERE id = %s", name, hostname, public_hostname, agent_key,int(port),int(id))
        else:
            self.db.execute(
                "INSERT INTO host (name,hostname,public_hostname,agent_key,port)"
                " VALUES (%s,%s,%s,%s,%s)",
                name,hostname,public_hostname,agent_key,port)
        self.redirect("/hosts/")
class HostListHandler(BaseHandler):
    def get(self):
        hosts = self.db.query("SELECT * FROM host ")
        self.render('host/list.html',hosts=hosts)

