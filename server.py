import tornado.ioloop
import tornado.web
import sqlite3
import pystache

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

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class SpecificHandler(tornado.web.RequestHandler):
    def __init__(self):
        super(tornado.web.RequestHandler, self).__init__(self)
        template = open("assets/template.html")
        self.templatestring = template.read()
    
    def get(self):
        result = pystache.render()
        self.write("Hello, world")

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
