import tornado.ioloop
import tornado.web
import sqlite3
import pystache
import os.path

conn = sqlite3.connect("assets/data.db")

class DB:
    @staticmethod
    def checkInit():
        c = conn.cursor()
        c.execute("""create table if not exists movies(
id INTEGER PUBLIC KEY,
name VARCHAR,
pathmpeg VARCHAR,
pathwebm VARCHAR,
pathoggv VARCHAR)""")
    
    @staticmethod
    def getAll():
        c = conn.cursor()
        c.execute("select * from movies")
        return list(c)

    @staticmethod
    def get(target):
        c = conn.cursor()
        c.execute("select * from movies where id=?", (target,))
        return tuple(c)

class WatchTemplate(pystache.View):
    

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class FaviconHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("")

class VideoHandler(tornado.web.RequestHandler):
    def get(self, target):
        self.write("")

class SpecificHandler(tornado.web.RequestHandler):
    def initialize(self):
        template = open("assets/template.html")
        self.templatestring = template.read()
    
    def get(self, target):
        result = pystache.render(self.templatestring, DB.get(target))
        self.write("You picked video number {0}".format(target))

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/favicon\.ico", FaviconHandler),
    (r"/videojs/(*)"
    (r"/videos/([a-z\.]+)", VideoHandler),
    (r"/view/([0-9]+)", SpecificHandler)
])

if __name__ == "__main__":
    DB.checkInit()
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
