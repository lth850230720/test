import tornado.web
from views import IndexHandler
import config
import os
class Application(tornado.web.Application):
    def __init__(self):
        handers=[
            #内部页面
            (r'/chatRoom',IndexHandler.ChatRoomHandler),
            #登陆页面
            (r'/login',IndexHandler.LoginHandler),
            #注册页面
            (r'/regist',IndexHandler.RegistHandler),
            #websocket入口
            (r'/chat',IndexHandler.ChatHandler),
            #用户名重复性验证
            (r'/userRegist',IndexHandler.UserRegistHandler),
            #基础页面，包括什么127.0.0.1:8000这种形式，类似www.baidu.com这种访问形式，需要放在路由表的最下边。
            # (r'/(.*)',IndexHandler.StaticFileHandler,{'path':os.path.join(config.BASE_DIRS,'static\\html'),'default_filename':'index.html'})
        ]
        super(Application,self).__init__(handers,**config.settings)
