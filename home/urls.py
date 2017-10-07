#coding=utf-8
from handlers.LoginHandler import (LoginHandler,RegisterHandler,IndexHandler,TestHandler,SMS_authHandler)

from handlers.MyHandler import MYHandler,AuthHandler,LogoutHandler
from handlers.HouseHandler import NewhouseHandler,MyHousesHandler,DetailHandler

from handlers.Up_information import Up_informationHandler,AvatrHandler,NameHandler
from handlers.HouseListHandler import SearchHandler
from handlers.OrdersHandler import BookingHandler,OrdersHandler,LordersHandler,AcceptOrderHandler,RejectOrderHandler,OrderCommentHandler


handlers = [
    (r'/register',RegisterHandler),                     #注册
    (r'/text', TestHandler),                            #图形验证码
    (r'/sms_auth', SMS_authHandler),                    #短信验证码
    (r'/login', LoginHandler),                          #登录
    (r'/index',IndexHandler),                           #主页
    (r'/up_information', Up_informationHandler),        #个人信息主页
    (r'/up_information/avatr', AvatrHandler),           #上传头像
    (r'/up_information/name', NameHandler),             #保存名字


    (r'/my', MYHandler),                                #我的家
    (r'/my/auth', AuthHandler),                         #实名验证
    (r'/my/logout', LogoutHandler),                     #退出登录


    (r'/myhouse', MyHousesHandler),                     #我的房源
    (r'/detail',DetailHandler),                         #房源详述
    (r'/newhouse', NewhouseHandler),                    #发布房源


    (r'/search', SearchHandler),                        #查看房源
    (r'/booking',BookingHandler),                       #预定
    (r'/lorders',LordersHandler),                       #客户订单
    (r'/orders',OrdersHandler),                         #我的订单
    (r'/acceptorder',AcceptOrderHandler),               #接单
    (r'/rejectorder',RejectOrderHandler),               #拒单
    (r'/ordercomment',OrderCommentHandler),             #评论


]