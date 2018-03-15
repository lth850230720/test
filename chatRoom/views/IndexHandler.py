import threading
import time
import tornado
import tornado.web
from tornado.web import RequestHandler
import config
import os
from tornado.httpclient import AsyncHTTPClient
import json
from tornado.websocket import WebSocketHandler
from config import settings
from db import sqlite_tornado


class RegistHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        username=self.get_argument("username")
        passwd=self.get_argument("passwd")
        mailNum=self.get_argument("mailNum")
        print(username,passwd,mailNum)
        self.userInsert(username,passwd,mailNum)
    # def userCheck(self,username,passwd,mailNum):
    #     cur=sqlite_tornado.get_db()
    #     cur.execute("select count(*) from user_table where user_name=? ",(username,))
    #     flag=cur.fetchall()[0][0]
    #     if flag==0:
    #         self.userInsert(cur,username,passwd,mailNum)
    #     else:
    #         cur.connection.close()
    #         self.write("user exists")
    def userInsert(self,username,passwd,mailNum):
        print(username,passwd,mailNum)
        cur=sqlite_tornado.get_db()
        cur.execute("insert into user_table values(?,?,?,?)",(None,username,passwd,mailNum))
        cur.connection.commit()
        cur.connection.close()
        self.write("regist success")

class LoginHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('login.html')
    def post(self, *args, **kwargs):
        username=self.get_argument("username")
        passwd=self.get_argument("passwd")
        print(username+passwd)
        #self.write(json.dumps([username,passwd]))
        flag=self.get_user(username,passwd)
        if flag:
            self.write({"flag":True})
        else:
            self.write({"flag":False})
    def get_user(self,username,passwd):
        cur=sqlite_tornado.get_db()
        cur.execute("select count(*) from user_table where user_name=? and user_passwd=? ",(username,passwd))
        flag=cur.fetchall()[0][0]
        cur.connection.close()
        if  flag==0:
            return False
        else:
            return True


class UserRegistHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        username=self.get_argument('username')
        cur=sqlite_tornado.get_db()
        cur.execute("select count(*) from user_table where user_name=? ",(username,))
        flag=cur.fetchall()[0][0]
        cur.connection.close()
        # print(flag)
        if flag==0:
            self.write({"flag":True})
        else:
            self.write({"flag":False})


class ChatRoomHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('qq_chat.html')
class ChatHandler(WebSocketHandler):
    #tornado的websocket模块
    #1.WebSocketHandler：处理通信
    #2.open()：当一个websocket链接建立后被调用
    #3.on_message():当客户端发送消息过来时调用
    #4.on_close():当websocket链接关闭后调用，客户端关闭
    #5.write_message(message,binary=False):
    #主动向客户端发送message消息，message可以是字符串或者是字典(自动转化为json字符串)
    #如果binary为False，则message会议UTF-8的编码发送，如果是TRUE，可以发送二进制模式，字节码
    #6.close():关闭websocket链接，服务器关闭
    #7.check_origin(origin):对于复合条件的请求源允许链接
    users=[]
    def open(self, *args, **kwargs):
        self.users.append(self)
        for user in self.users:
            user.write_message(self.request.remote_ip)
        print(self.users)
        print("***********************")
    #当关闭浏览器，客户端退出链接，调用此方法
    def on_close(self):
        self.users.remove(self)
        for user in self.users:
            print(user)
            user.write_message("%s已退出群聊"%(self.request.remote_ip))
    #
    def on_message(self, message):
        for user in self.users:
            print(user)
            user.write_message('%s说%s'%(self.request.remote_ip,message))

    def check_origin(self, origin):
        return True




#装饰器协程原理
# def genCoroutine(func):
#     def wrapper(*args,**kwargs):
#         gen1=func()
#         gen2=next(gen1)
#         def run(g):
#             res=next(g)
#             try:
#                 gen1.send(res)
#             except StopIteration as e:
#                 pass
#         threading.Thread(target=run,args=(gen2,)).start
#     return wrapper