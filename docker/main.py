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

define("port", default=8889, help="run on the given port", type=int)

import tornado

from images.image import ImageHandler

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", ImageHandler),
            (r"/image", ImageHandler),

        ]
        settings = dict(
            blog_title=u"Tornado Blog",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()