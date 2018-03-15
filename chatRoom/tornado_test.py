import tornado
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from application import Application
from db import sqlite_tornado
if __name__ == '__main__':
    app=Application()
    httpserver=tornado.httpserver.HTTPServer(app)
    httpserver.bind(8080)
    sqlite_tornado.db_init()
    httpserver.start()
    tornado.ioloop.IOLoop.instance().start()



