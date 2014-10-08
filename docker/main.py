#coding: utf-8
__author__ = 'aaron'
import os
import markdown
import os.path
import re
import torndb
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.escape
import unicodedata

from tornado.options import define, options
from tornado.escape import url_unescape

define("mysql_host", default="10.0.31.81:3306", help="dockermanager database host")
define("mysql_database", default="dockermanager", help="dockermanager database name")
define("mysql_user", default="root", help="dockermanager database user")
define("mysql_password", default="root", help="dockermanager database password")
define("port", default=8888, help="run on the given port", type=int)

import tornado

from images.views import ImageListHandler,ImageHandler
from hosts.views import HostHandler,HostListHandler
from containers.views import ContainerListHandler,ContainerHandler

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HostListHandler),
            (r"/host/", HostHandler),
            (r"/hosts/", HostListHandler),

            (r"/images/", ImageListHandler),
            (r"/image/(?P<hid>\w+)/(?P<iid>\w+)/(?P<op>\w+)", ImageHandler),
            (r"/image/(?P<hid>\w+)/(?P<iid>\w+)", ImageHandler),

            (r"/containers/",ContainerListHandler),
            (r"/containers/(?P<hid>\w+)/(?P<cid>\w+)/(?P<op>\w+)",ContainerHandler),
            (r"/containers/(?P<hid>\w+)/(?P<cid>\w+)",ContainerHandler),

        ]
        settings = dict(
            title=u"Docker管理工具",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        self.db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()