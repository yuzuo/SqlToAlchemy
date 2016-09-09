#!/usr/bin/env python
import os.path
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

from handlers.search_handler import SearchHandler

define("port", default=9800, help="run on the given port", type=int)

from handlers.commonHandler import BaseHandler, CodeHandler, TableOPTSHomeHandler, TableOPTSHandler


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/opts/(.*)", TableOPTSHandler),
            (r"/", TableOPTSHomeHandler),
            (r"/ops/code/([\w\W]*)", CodeHandler),
        ]

        settings = dict(
            blog_title=u"MySQL OPTS",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            autoescape=None,
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            login_url="/auth/login",
            debug=True,
        )

        tornado.web.Application.__init__(self, handlers, **settings)

        # Have one global connection to the blog DB across all handlers
        # self.db = torndb.Connection(
        #     host=options.mysql_host, database=options.mysql_database,
        #     user=options.mysql_user, password=options.mysql_password)


class NotFoundHandler(BaseHandler):
    def get(self):
        self.render('404.html')


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    print 'http://localhost:9800'
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
