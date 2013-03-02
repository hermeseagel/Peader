#-*-coding:utf-8 -*-

import copy
import MySQLdb
import MySQLdb.constants
import MySQLdb.converters
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options



from models import model

import os.path
from controllers import  LoginHandler,AvatarHandler,RegisterHandler

from tornado.options import define, options

define("port", default = 8000, help  = "run on given port", type = int)
define("mysql_host", default = "localhost", help = "blog database host")
define("mysql_database", default = "rss_db", help = "rss server database name")
define("mysql_user", default = "root", help = "rss server database user")
define("mysql_password", default = "thomas", help="rss server database password")
define("mysql_port", default = 3036, help="rss server database port", type = int)


class RssWebReaderApp(tornado.web.Application):
    """这个是阅读器的主应用类，功能增加：
    1.请求控制开关
    2.监控功能开关
    3.数据库链接参数
    """
    
    def __init__(self):
        
        handlers = [
                    (r'/login', LoginHandler.LoginHandler),
                    (r'/register', RegisterHandler.RegisterHandler),
                    (r'/avatar', AvatarHandler.AvatarHandler),
                    
                    
                    ]
        
        settings = dict(
                    static_path = os.path.join(os.path.dirname(__file__), "static"),
                    template_path = os.path.join(os.path.dirname(__file__), "templates"),
                    debug = True,
                    cookie_secret = "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
                    #login_url = r'/noperm',
                   )
        
        #数据库连接参数配置
        self.db_settings = dict(
                               use_unicode = True, 
                                   charset = "utf8",
                                      host = options.mysql_host, 
                                        db = options.mysql_database,
                                     user  = options.mysql_user, 
                                    passwd = options.mysql_password,
                               )
        
        model.Model.initailize(self.db_settings)
        
        tornado.web.Application.__init__(self, handlers, **settings)



if __name__ == "__main__":
    
    tornado.options.parse_command_line()
    
    server = tornado.httpserver.HTTPServer(RssWebReaderApp())
    
    server.listen(options.port)
    
    tornado.ioloop.IOLoop.instance().start()
    
    
    