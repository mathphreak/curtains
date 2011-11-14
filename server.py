import tornado.ioloop
import tornado.web
import sqlite3
import pystache
import os.path
import time
import math
import shutil

video_file_extension = "mp4"

conn = sqlite3.connect("assets/data.db")

class DB:    
    @staticmethod
    def checkInit():
        c = conn.cursor()
        c.execute("""create table if not exists movies(
id INTEGER PUBLIC KEY ASC,
name VARCHAR,
file BLOB)""")

    @staticmethod
    def forceInit():
        c = conn.cursor()
        c.execute("drop table movies")
        c.execute("""create table movies(
id INTEGER PUBLIC KEY ASC,
name VARCHAR,
file BLOB)""")
    
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

    @staticmethod
    def add(name, path):
        maxx = max([idd for idd, name in DB.getAll()] + [-1])
        shutil.copy2(path, "videos/" + str(maxx) + "." + path.split(".")[-1])
        c = conn.cursor()
        c.execute("insert into movies values(?, ?)", (maxx + 1, name))
        return

class Watch(pystache.View):
    def __init__(self, tupl):
        super(pystache.View, self).__init__()
        self.context_list = []
        self.formstr = "/videos/{0}.{1}?{2}"
        try:
            self.id, self.name, blob = tupl
        except ValueError:
            self.id = 3
            self.name = ""

    def __formt__(self, name):
        return self.formstr.format(self.id, name, math.floor(time.time()))

    def name(self):
        return self.name
    
    def mp4(self):
        return self.__formt__("mp4")
    
    def webm(self):
        return self.__formt__("webm")

    def ogv(self):
        return self.__formt__("ogv")

class Index(pystache.View):
    def movies(self):
        formstr = "/view/{0}"
        class MovieObject:
            def __init__(self, idd, name):
                self.id = idd
                self.name = name

            def watchpath(self):
                return formstr.format(self.id)
        
        allMovies = DB.getAll()
        return [MovieObject(idd, name) for idd, name in allMovies]

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        result = Index().render()
        self.write(result)

class FaviconHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("")

class VideoHandler(tornado.web.RequestHandler):
    def get(self, target, ext):
        print("GET /videos/", target, ".", ext, sep="")
        if ext == video_file_extension:
            self.write(DB.get(target)[2])
            return
        self.write(str(target) + " dot " + str(ext))

class SpecificHandler(tornado.web.RequestHandler):
    def get(self, target):
        print("GET /view/", target, sep="")
        result = Watch(DB.get(target)).render()
        self.write(result)

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/favicon\.ico", FaviconHandler),
    (r"/videos/([0-9]+\.\w{3,4}.*)", tornado.web.StaticFileHandler, dict(
        path="videos"
    )),
    (r"/view/([0-9]+)", SpecificHandler)
], static_path=os.path.join(os.path.dirname(__file__), "static"))

if __name__ == "__main__":
    DB.checkInit()
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
